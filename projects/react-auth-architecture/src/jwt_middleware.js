/**
 * JWT Authentication Middleware
 * 
 * This middleware intercepts incoming HTTP requests to protected routes.
 * It extracts the JSON Web Token from the 'Authorization' header, 
 * verifies its cryptographic signature, and attaches the decoded user 
 * payload to the request object for downstream use.
 */

const jwt = require('jsonwebtoken');

const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return res.status(401).json({ 
            error: 'Access denied. No token provided.' 
        });
    }

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;
        
        next();
    } catch (error) {
        return res.status(403).json({ 
            error: 'Invalid or expired token.' 
        });
    }
};

module.exports = authenticateToken;