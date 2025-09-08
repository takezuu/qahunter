package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type project struct {
	ID    string `json:"id"`
	Title string `json:"title"`
}

var projects = []project{
	{ID: "1", Title: "Roma's IPO"},
	{ID: "2", Title: "Microsoft shop"},
	{ID: "3", Title: "Apple juice"},
}

func getProjects(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, projects)
}

func main() {
	router := gin.Default()
	router.GET("/projects", getProjects)

	router.Run(":8080")
}
