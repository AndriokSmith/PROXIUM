package main

import (
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"log"
	"net/http"
)

func getPage(url string) *http.Response {
	res, err := http.Get(url)
	if err != nil {
		log.Fatal(err)
	}
	return res
}

func getHosts(res *http.Response) []string {
	doc, err := goquery.NewDocumentFromReader(res.Body)
	if err != nil {
		log.Fatal(err)
	}

	hosts := []string{}

	doc.Find("td").Each(func(_ int, s *goquery.Selection) {
		row := string(s.Text())
		for i := 0; i < len(row); i++ {
			if string(row[i]) == "." {
				hosts = append(hosts, row+"\n")
				break
			}
		}

	})
	return hosts
}

func main() {
	page := getPage("https://free-proxy-list.net/")
	allHosts := getHosts(page)
	fmt.Print(allHosts)
}
