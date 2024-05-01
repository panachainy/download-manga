package main

import (
	"fmt"
	"io/fs"
	"io/ioutil"
	"log"
	"os"
)

func main() {
	const configFolder = "./configs/"

	// read configs
	var folders = get_files_from_folder(configFolder)
	for _, folder := range folders {
		fmt.Println(folder.Name())
		var files = get_files_from_folder(configFolder + folder.Name())
		for _, file := range files {
			var bodyData = read_file(configFolder + folder.Name() + "/" + file.Name())
			fmt.Println(bodyData)
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

// func download_file(url string) {
// 	// code to download file
// }
