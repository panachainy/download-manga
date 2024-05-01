package main

import (
	"fmt"
	"io/fs"
	"log"
	"os"
)

func main() {
	// configs/Silent War สงครามแห่งกามราคะ/ตอนที่ 136.json

	// read configs
	var folders = get_files_from_folder("./configs")
	for _, folder := range folders {
		fmt.Println(folder.Name())
	}
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
