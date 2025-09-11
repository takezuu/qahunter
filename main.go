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
	router.GET("/projects/:id", getProjectByID)
	router.POST("/projects", postProjects)

	router.Run(":8080")
}

func postProjects(c *gin.Context) {
	var newProject project

	// Call BindJSON to bind the received JSON to
	// newProject.
	if err := c.BindJSON(&newProject); err != nil {
		return
	}

	// Add the new album to the slice.
	projects = append(projects, newProject)
	c.IndentedJSON(http.StatusCreated, newProject)
}

func getProjectByID(c *gin.Context) {
	id := c.Param("id")

	// Loop over the list of albums, looking for
	// an album whose ID value matches the parameter.
	for _, p := range projects {
		if p.ID == id {
			c.IndentedJSON(http.StatusOK, p)
			return
		}
	}
	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "project not found"})
}
