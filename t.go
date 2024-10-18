package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
)

func main() {
	r := gin.Default()

	r.GET("/", func(c *gin.Context) {
		for i := 0; i < 10000; i++ {
			fmt.Print(i)
		}
		c.JSON(http.StatusOK, gin.H{
			"message": "¡Hola, mundo!",
		})
	})

	r.Run("0.0.0.0:8080") // Only input dev
}
