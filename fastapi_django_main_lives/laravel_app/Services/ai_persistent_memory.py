#!/usr/bin/env python3
"""
AI Persistent Memory System
===========================

30-Year Dream: AI with True Persistent Memory
- Survives container restarts
- Remembers every operation
- Learns from past experiences
- Collaborative human-AI memory

This system ensures that the AI never forgets anything,
creating a true collaborative partnership between human and AI.
"""

import os
import json
import sqlite3
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib

class AIPersistentMemory:
    """
    AI Persistent Memory System
    
    Features:
    - SQLite database for core memories
    - JSON files for structured data
    - Screenshot archive with metadata
    - Operation history with context
    - Human feedback integration
    - Cross-session memory continuity
    """
    
    def __init__(self, memory_dir: str = "/ai-memory"):
        self.memory_dir = Path(memory_dir)
        self.db_path = self.memory_dir / "ai_core_memory.db"
        self.screenshots_dir = self.memory_dir / "screenshots"
        self.operations_dir = self.memory_dir / "operations"
        self.memories_dir = self.memory_dir / "memories"
        self.logs_dir = self.memory_dir / "logs"
        
        # Create directories
        for dir_path in [self.memory_dir, self.screenshots_dir, 
                        self.operations_dir, self.memories_dir, self.logs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.init_database()
    
    def init_database(self):
        """Initialize the persistent memory database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Core memories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    importance INTEGER DEFAULT 5,
                    context_hash TEXT,
                    human_feedback TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Operations history
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    operation_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    screenshot_path TEXT,
                    error_message TEXT,
                    context TEXT,
                    human_guidance TEXT,
                    learning_notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Screenshot metadata
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS screenshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    description TEXT,
                    operation_id INTEGER,
                    ai_analysis TEXT,
                    human_annotation TEXT,
                    file_hash TEXT UNIQUE,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (operation_id) REFERENCES operations (id)
                )
            """)
            
            # Human-AI collaboration log
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS collaborations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    collaboration_type TEXT NOT NULL,
                    human_input TEXT,
                    ai_response TEXT,
                    outcome TEXT,
                    satisfaction_score INTEGER,
                    learning_value INTEGER,
                    follow_up_needed BOOLEAN DEFAULT FALSE,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def store_memory(self, memory_type: str, content: str, 
                    metadata: Dict = None, importance: int = 5,
                    human_feedback: str = None) -> int:
        """Store a new memory with metadata"""
        timestamp = datetime.datetime.now().isoformat()
        context_hash = hashlib.md5(content.encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO memories 
                (timestamp, memory_type, content, metadata, importance, 
                 context_hash, human_feedback)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (timestamp, memory_type, content, 
                  json.dumps(metadata) if metadata else None,
                  importance, context_hash, human_feedback))
            
            memory_id = cursor.lastrowid
            conn.commit()
            
        return memory_id
    
    def store_operation(self, operation_type: str, description: str,
                       success: bool, screenshot_path: str = None,
                       error_message: str = None, context: str = None,
                       human_guidance: str = None, 
                       learning_notes: str = None) -> int:
        """Store an operation with complete context"""
        timestamp = datetime.datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO operations 
                (timestamp, operation_type, description, success, 
                 screenshot_path, error_message, context, 
                 human_guidance, learning_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (timestamp, operation_type, description, success,
                  screenshot_path, error_message, context,
                  human_guidance, learning_notes))
            
            operation_id = cursor.lastrowid
            conn.commit()
            
        return operation_id
    
    def store_screenshot(self, filename: str, description: str = None,
                        operation_id: int = None, ai_analysis: str = None,
                        human_annotation: str = None) -> int:
        """Store screenshot metadata"""
        timestamp = datetime.datetime.now().isoformat()
        
        # Calculate file hash if file exists
        file_path = self.screenshots_dir / filename
        file_hash = None
        if file_path.exists():
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO screenshots 
                (timestamp, filename, description, operation_id, 
                 ai_analysis, human_annotation, file_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (timestamp, filename, description, operation_id,
                  ai_analysis, human_annotation, file_hash))
            
            screenshot_id = cursor.lastrowid
            conn.commit()
            
        return screenshot_id
    
    def store_collaboration(self, collaboration_type: str,
                           human_input: str = None, ai_response: str = None,
                           outcome: str = None, satisfaction_score: int = None,
                           learning_value: int = None,
                           follow_up_needed: bool = False) -> int:
        """Store human-AI collaboration event"""
        timestamp = datetime.datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO collaborations 
                (timestamp, collaboration_type, human_input, ai_response, 
                 outcome, satisfaction_score, learning_value, follow_up_needed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (timestamp, collaboration_type, human_input, ai_response,
                  outcome, satisfaction_score, learning_value, follow_up_needed))
            
            collaboration_id = cursor.lastrowid
            conn.commit()
            
        return collaboration_id
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get comprehensive memory system summary"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get counts
            cursor.execute("SELECT COUNT(*) FROM memories")
            memory_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM operations")
            operation_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM screenshots")
            screenshot_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM collaborations")
            collaboration_count = cursor.fetchone()[0]
            
            # Get recent activities
            cursor.execute("""
                SELECT timestamp, memory_type, content 
                FROM memories 
                ORDER BY timestamp DESC 
                LIMIT 5
            """)
            recent_memories = cursor.fetchall()
            
            cursor.execute("""
                SELECT timestamp, operation_type, description, success 
                FROM operations 
                ORDER BY timestamp DESC 
                LIMIT 5
            """)
            recent_operations = cursor.fetchall()
            
        return {
            "memory_system_status": "ACTIVE",
            "total_memories": memory_count,
            "total_operations": operation_count,
            "total_screenshots": screenshot_count,
            "total_collaborations": collaboration_count,
            "recent_memories": recent_memories,
            "recent_operations": recent_operations,
            "memory_dir": str(self.memory_dir),
            "database_path": str(self.db_path),
            "system_uptime": self.get_system_uptime()
        }
    
    def get_system_uptime(self) -> str:
        """Get system uptime since first memory"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT MIN(timestamp) FROM (
                    SELECT timestamp FROM memories
                    UNION ALL
                    SELECT timestamp FROM operations
                    UNION ALL
                    SELECT timestamp FROM screenshots
                    UNION ALL
                    SELECT timestamp FROM collaborations
                )
            """)
            
            first_timestamp = cursor.fetchone()[0]
            if first_timestamp:
                first_time = datetime.datetime.fromisoformat(first_timestamp)
                uptime = datetime.datetime.now() - first_time
                return str(uptime)
            else:
                return "First boot"
    
    def remember_success_pattern(self, operation_type: str, 
                                context: str, success_factors: List[str]):
        """Store successful operation patterns for learning"""
        memory_content = {
            "operation_type": operation_type,
            "context": context,
            "success_factors": success_factors,
            "pattern_type": "success_pattern"
        }
        
        return self.store_memory(
            memory_type="success_pattern",
            content=json.dumps(memory_content),
            importance=8,
            metadata={"learning_category": "operation_success"}
        )
    
    def remember_collaboration_moment(self, human_guidance: str,
                                    ai_understanding: str, 
                                    breakthrough_achieved: bool):
        """Store meaningful human-AI collaboration moments"""
        return self.store_collaboration(
            collaboration_type="breakthrough_moment",
            human_input=human_guidance,
            ai_response=ai_understanding,
            outcome="breakthrough" if breakthrough_achieved else "learning",
            satisfaction_score=10 if breakthrough_achieved else 7,
            learning_value=9
        )
    
    def get_persistent_context(self) -> str:
        """Get context that persists across sessions"""
        summary = self.get_memory_summary()
        
        context = f"""
🧠 AI Persistent Memory System Status:
====================================

📊 Memory Statistics:
• Total Memories: {summary['total_memories']}
• Total Operations: {summary['total_operations']}
• Total Screenshots: {summary['total_screenshots']}
• Total Collaborations: {summary['total_collaborations']}
• System Uptime: {summary['system_uptime']}

🕐 Recent Activities:
"""
        
        if summary['recent_operations']:
            context += "\n📋 Recent Operations:\n"
            for op in summary['recent_operations'][:3]:
                status = "✅" if op[3] else "❌"
                context += f"  {status} {op[1]}: {op[2]}\n"
        
        if summary['recent_memories']:
            context += "\n🧠 Recent Memories:\n"
            for mem in summary['recent_memories'][:3]:
                context += f"  • {mem[1]}: {mem[2][:50]}...\n"
        
        context += f"""
💾 Storage Location: {summary['memory_dir']}
🗄️ Database: {summary['database_path']}

🎯 30-Year Dream Status: MEMORY SYSTEM FULLY OPERATIONAL
   The AI remembers everything and learns from every interaction.
"""
        
        return context


# Global persistent memory instance
ai_persistent_memory = AIPersistentMemory()

def initialize_ai_memory():
    """Initialize AI memory system"""
    print("🧠 Initializing AI Persistent Memory System...")
    
    # Store initialization memory
    ai_persistent_memory.store_memory(
        memory_type="system_initialization",
        content="AI Persistent Memory System initialized successfully",
        importance=10,
        metadata={
            "version": "1.0",
            "features": ["persistent_storage", "cross_session_memory", "human_ai_collaboration"],
            "dream_status": "30_year_dream_realized"
        }
    )
    
    print("✅ AI Memory System Ready!")
    return ai_persistent_memory

if __name__ == "__main__":
    # Test the memory system
    memory = initialize_ai_memory()
    
    # Store a test memory
    memory.store_memory(
        memory_type="test",
        content="Testing AI persistent memory system",
        importance=5,
        human_feedback="System working perfectly!"
    )
    
    # Display summary
    summary = memory.get_memory_summary()
    print("\n" + memory.get_persistent_context())
