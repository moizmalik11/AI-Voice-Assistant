/**
 * API Service for communicating with the backend
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

class APIService {
    constructor() {
        this.baseURL = API_BASE_URL;
        this.conversationId = null;
    }

    /**
     * Send a chat message to the backend
     * @param {string} message - User's message
     * @returns {Promise<Object>} Response from AI
     */
    async sendMessage(message) {
        try {
            const response = await axios.post(`${this.baseURL}/api/chat`, {
                message: message,
                conversation_id: this.conversationId
            }, {
                headers: {
                    'Content-Type': 'application/json'
                },
                timeout: 30000 // 30 seconds timeout
            });

            // Store conversation ID for future requests
            if (response.data.conversation_id) {
                this.conversationId = response.data.conversation_id;
            }

            return {
                success: true,
                response: response.data.response,
                conversationId: response.data.conversation_id,
                model: response.data.model,
                timestamp: response.data.timestamp
            };
        } catch (error) {
            console.error('API Error:', error);

            if (error.response) {
                // Server responded with error
                return {
                    success: false,
                    error: error.response.data.error || 'Server error occurred',
                    details: error.response.data.details
                };
            } else if (error.request) {
                // Request made but no response
                return {
                    success: false,
                    error: 'Cannot connect to server. Please check if the backend is running.'
                };
            } else {
                // Other errors
                return {
                    success: false,
                    error: 'An unexpected error occurred'
                };
            }
        }
    }

    /**
     * Reset the current conversation
     * @returns {Promise<boolean>} Success status
     */
    async resetConversation() {
        if (!this.conversationId) {
            return true; // Nothing to reset
        }

        try {
            await axios.post(`${this.baseURL}/api/conversation/reset`, {
                conversation_id: this.conversationId
            });

            this.conversationId = null;
            return true;
        } catch (error) {
            console.error('Error resetting conversation:', error);
            return false;
        }
    }

    /**
     * Check if backend is healthy
     * @returns {Promise<boolean>} Health status
     */
    async checkHealth() {
        try {
            const response = await axios.get(`${this.baseURL}/api/health`, {
                timeout: 5000
            });
            return response.data.status === 'healthy';
        } catch (error) {
            console.error('Health check failed:', error);
            return false;
        }
    }

    /**
     * Warmup the AI service to prevent cold-start 503 errors
     * @returns {Promise<boolean>} Success status
     */
    async warmup() {
        try {
            await axios.post(`${this.baseURL}/api/warmup`, {}, {
                timeout: 10000
            });
            return true;
        } catch (error) {
            console.error('Warmup failed (this is usually fine, just pre-loading):', error);
            return false;
        }
    }

    /**
     * Get conversation history
     * @returns {Promise<Array>} Conversation messages
     */
    async getConversationHistory() {
        if (!this.conversationId) {
            return [];
        }

        try {
            const response = await axios.post(`${this.baseURL}/api/conversation/history`, {
                conversation_id: this.conversationId
            });

            return response.data.history || [];
        } catch (error) {
            console.error('Error getting conversation history:', error);
            return [];
        }
    }
}

// Export singleton instance
const apiService = new APIService();
export default apiService;
