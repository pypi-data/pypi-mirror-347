"""
Neo4j Client Adapter for Knowledge v1

Provides minimal interface for connecting to and querying the Neo4j database.
"""

import os
from typing import Dict, List, Any, Optional, Union
import neo4j

class Neo4jConnectionError(Exception):
    """Exception raised for Neo4j connection issues."""
    pass

class Neo4jQueryError(Exception):
    """Exception raised for Neo4j query execution issues."""
    pass

class Neo4jClient:
    """Minimal Neo4j client for Knowledge v1 system."""
    
    def __init__(self, uri=None, username=None, password=None, database="neo4j"):
        """Initialize Neo4j client with connection details.
        
        If not provided, the following environment variables are used:
        - NEO4J_URI
        - NEO4J_USER
        - NEO4J_PASS
        - NEO4J_DATABASE (optional, default: "neo4j")
        """
        self.uri = uri or os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        self.username = username or os.environ.get("NEO4J_USER", "neo4j")
        self.password = password or os.environ.get("NEO4J_PASS", "password")
        self.database = database or os.environ.get("NEO4J_DATABASE", "neo4j")
        self._driver = None
    
    def connect(self):
        """Connect to Neo4j database."""
        if not self._driver:
            try:
                self._driver = neo4j.GraphDatabase.driver(
                    self.uri, 
                    auth=(self.username, self.password)
                )
                # Test connection
                with self._driver.session(database=self.database) as session:
                    session.run("RETURN 1")
            except Exception as e:
                raise Neo4jConnectionError(f"Failed to connect to Neo4j: {str(e)}")
        return self._driver
    
    def close(self):
        """Close the Neo4j connection."""
        if self._driver:
            self._driver.close()
            self._driver = None
    
    def run_query(self, query, parameters=None):
        """Run a Cypher query and return results.
        
        Args:
            query: Cypher query string
            parameters: Optional parameters for query
            
        Returns:
            List of records from query result
        """
        driver = self.connect()
        try:
            with driver.session(database=self.database) as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            raise Neo4jQueryError(f"Error executing query: {str(e)}")
    
    def is_connected(self):
        """Check if connected to Neo4j database."""
        if not self._driver:
            return False
        
        try:
            with self._driver.session(database=self.database) as session:
                result = session.run("RETURN 1 as test")
                return result.single()["test"] == 1
        except Exception:
            return False
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close() 