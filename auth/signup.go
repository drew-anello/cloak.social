package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type SignupRequest struct {
	Email    string `json:"email" binding:"required"`
	Password string `json:"password" binding:"required"`
	Name     string `json:"name" binding:"required"`
}

func HandleSignup(c *gin.Context) {
	var signup SignupRequest
	if err := c.ShouldBindJSON(&signup); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// hashedPassword, err := utils.HashPassword(signup.Password)
	// if err != nil {
	// 	c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to hash password"})
	// 	return
	// }

	// TODO: Save user to database
	// For now, return success
	c.JSON(http.StatusOK, gin.H{"message": "Signup successful"})
}
