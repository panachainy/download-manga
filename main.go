package main

import (
	"download-manga/cmd"
	"encoding/json"
	"fmt"
	"io"
	"io/fs"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os"
	"regexp"
	"strings"
	"sync"
	"time"

	"github.com/spf13/cobra"
)

const retryFolder = "configs/retries"
const retryDownloaded = "./configDownloaded/retries"

type ChapterConfig struct {
	FullPath string `json:"full_path"`
	Url      string `json:"url"`
}

func main() {
	var loadDownload = &cobra.Command{
		Use:   "download",
		Short: "Download manga from config",
		Run: func(cmd *cobra.Command, args []string) {
			// task := args[0]
			// fmt.Printf("Added task: %s\n", task)
			LoadDownload()
		},
	}

	var loadRetry = &cobra.Command{
		Use:   "retry",
		Short: "Retry download manga from config",
		Run: func(cmd *cobra.Command, args []string) {
			// task := args[0]
			// fmt.Printf("Added task: %s\n", task)
			LoadRetry()
		},
	}

	cmd.RootCmd.AddCommand(loadDownload)
	cmd.RootCmd.AddCommand(loadRetry)

	cmd.Execute()
}

// func main() {
// 	// LoadDownload()
// 	LoadRetry()
// }

func LoadRetry() {
	files := getFilesFromFolder(retryFolder)
	for _, file := range files {
		var chapterConfig = getChapterConfig(retryFolder + "/" + file.Name())
		var wg sync.WaitGroup

		for _, config := range chapterConfig {
			wg.Add(1)
			go download_file(config.Url, config.FullPath, &wg, func() {
				os.Rename(retryFolder+"/"+file.Name(), retryDownloaded+"/"+file.Name())
			}, true)
		}
		wg.Wait()
	}
}

// TODO: make it command
func LoadDownload() {
	const configFolder = "./configs/"
	const destinationFolder = "./pdfs/"
	const configDownloaded = "./configDownloaded/"

	// create fodler
	os.Mkdir(destinationFolder, 0755)

	// read configs
	var folders = getFilesFromFolder(configFolder)
	for _, folder := range folders {
		os.Mkdir(destinationFolder+folder.Name(), 0755)

		var files = getFilesFromFolder(configFolder + folder.Name())
		for _, file := range files {
			folderName := destinationFolder + folder.Name() + "/" + strings.Split(file.Name(), ".json")[0]

			os.Mkdir(folderName, 0755)
			var chapterConfigs = getChapterConfig(configFolder + folder.Name() + "/" + file.Name())
			var wg sync.WaitGroup

			for _, chapterConfig := range chapterConfigs {
				wg.Add(1)
				go download_file(chapterConfig.Url, chapterConfig.FullPath, &wg, func() {}, false)
			}

			wg.Wait()
		}
		// move config to configDownloaded
		os.Rename(configFolder+folder.Name(), configDownloaded+folder.Name())
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

func getChapterConfig(filePath string) []ChapterConfig {
	var jsonStr = read_file(filePath)

	var chapterConfig []ChapterConfig
	err := json.Unmarshal([]byte(jsonStr), &chapterConfig)
	if err != nil {
		log.Fatalf("Error unmarshaling JSON: %v", err)
	}

	return chapterConfig
}

func getFilesFromFolder(directory_url string) []fs.FileInfo {
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

func download_file(url string, path string, wg *sync.WaitGroup, cb func(), is_retry_mode bool) {
	defer wg.Done()

	// Specify the URL of the file you want to download
	fileURL := url

	// Create a new file for writing the downloaded content
	file, err := os.Create(path)
	if err != nil {
		fmt.Println("Error creating file:", err)
		if !is_retry_mode {
			logErrorConfig(url, path)
		}
		return
	}
	defer file.Close()

	// Make the HTTP GET request
	resp, err := http.Get(fileURL)

	// handle case invalid character "\\"
	if err != nil && strings.Contains(err.Error(), `invalid character "\\" in host name`) {
		fmt.Println(`[case] Is invalid character "\\" case`, fileURL)

		newFileURL := regexp.MustCompile(`\\`).ReplaceAllString(fileURL, "")
		// fmt.Println(newFileURL)
		resp, err = http.Get(newFileURL)
	}

	if err != nil {

		fmt.Println("Error downloading file:", err)
		if !is_retry_mode {
			logErrorConfig(url, path)
		}
		return
	}
	defer resp.Body.Close()

	// Copy the file content to the local file
	_, err = io.Copy(file, resp.Body)
	if err != nil {
		fmt.Println("Error writing to file:", err)
		if !is_retry_mode {
			logErrorConfig(url, path)
		}
		return
	}

	fmt.Println("File downloaded:", path)

	cb()
}

func logErrorConfig(url string, path string) {
	var chapterConfig = ChapterConfig{
		FullPath: path,
		Url:      url,
	}

	var chapterConfigs = []ChapterConfig{chapterConfig}
	logFile := fmt.Sprintf(retryFolder+"/%v.json", generateRandomString(9))

	os.MkdirAll(retryFolder, 0755)
	file, err := os.Create(logFile)

	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(chapterConfigs); err != nil {
		fmt.Println("Error encoding JSON:", err)
		return
	}
}

const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

var seededRand *rand.Rand = rand.New(rand.NewSource(time.Now().UnixNano()))

func generateRandomString(length int) string {
	b := make([]byte, length)
	for i := range b {
		b[i] = charset[seededRand.Intn(len(charset))]
	}
	return string(b)
}
