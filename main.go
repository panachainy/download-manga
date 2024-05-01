package main

import (
	"encoding/json"
	"fmt"
	"io"
	"io/fs"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"sync"
)

type ChapterConfig struct {
	FullPath string `json:"full_path"`
	Url      string `json:"url"`
}

func main() {
	const configFolder = "./configs/"
	const destinationFolder = "./pdfs/"

	// create fodler
	os.Mkdir(destinationFolder, 0755)

	// read configs
	var folders = get_files_from_folder(configFolder)
	for _, folder := range folders {
		os.Mkdir(destinationFolder+folder.Name(), 0755)

		var files = get_files_from_folder(configFolder + folder.Name())
		for _, file := range files {
			os.Mkdir(destinationFolder+folder.Name()+"/"+strings.Split(file.Name(), ".")[0], 0755)
			var chapterConfigs = get_chapter_config(configFolder + folder.Name() + "/" + file.Name())
			var wg sync.WaitGroup

			for _, chapterConfig := range chapterConfigs {
				wg.Add(1)
				go download_file(chapterConfig.Url, chapterConfig.FullPath, &wg)
			}

			wg.Wait()

			break
		}
	}
}

func read_file(filePath string) string {
	// Read the content of the file
	data, err := ioutil.ReadFile(filePath)
	if err != nil {
		log.Fatalf("Error reading file: %v", err)
	}

	return string(data)
}

func get_chapter_config(filePath string) []ChapterConfig {
	var jsonStr = read_file(filePath)

	var chapterConfig []ChapterConfig
	err := json.Unmarshal([]byte(jsonStr), &chapterConfig)
	if err != nil {
		log.Fatalf("Error unmarshaling JSON: %v", err)
	}

	return chapterConfig
}

func get_files_from_folder(directory_url string) []fs.FileInfo {
	// Open the directory to read its contents
	files, err := os.Open(directory_url)
	if err != nil {
		log.Println("Error opening directory:", err)
		return nil
	}
	defer files.Close()

	// Read the files from the directory
	fileInfos, err := files.Readdir(-1)
	if err != nil {
		log.Println("Error reading directory:", err)
		return nil
	}

	return fileInfos
}

func download_file(url string, path string, wg *sync.WaitGroup) {
	defer wg.Done()

	// Specify the URL of the file you want to download
	fileURL := url

	// Extract the file name from the URL
	// fileName := filepath.Base(fileURL)

	// Create a new file for writing the downloaded content
	file, err := os.Create(path)
	if err != nil {
		fmt.Println("Error creating file:", err)
		return
	}
	defer file.Close()

	// Make the HTTP GET request
	resp, err := http.Get(fileURL)
	if err != nil {
		fmt.Println("Error downloading file:", err)
		return
	}
	defer resp.Body.Close()

	// Copy the file content to the local file
	_, err = io.Copy(file, resp.Body)
	if err != nil {
		fmt.Println("Error writing to file:", err)
		return
	}

	fmt.Println("File downloaded:", path)
}
