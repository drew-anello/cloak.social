package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type LoginRequest struct {
	Email    string `json:"email" binding:"required"`
	Password string `json:"password" binding:"required"`
}

func HandleLogin(c *gin.Context) {
	var login LoginRequest
	if err := c.ShouldBindJSON(&login); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// TODO: Get user from database and verify password
	// For now, return success
	c.JSON(http.StatusOK, gin.H{"message": "Login successful"})
}
