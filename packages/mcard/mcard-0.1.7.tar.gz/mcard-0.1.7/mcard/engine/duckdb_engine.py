import duckdb
from typing import Optional
import logging
import os
from mcard.model.card import MCard, MCardFromData
from mcard.model.card_collection import Page
from mcard.engine.base import StorageEngine, DatabaseConnection
from mcard.config.config_constants import DEFAULT_PAGE_SIZE, TRIGGERS
from mcard.model.schema import CARD_TABLE_SCHEMA

logger = logging.getLogger(__name__)

class DuckDBConnection(DatabaseConnection):
    def __init__(self, db_path: str):
        self.db_path = os.path.abspath(db_path)
        self.conn: Optional[duckdb.DuckDBPyConnection] = None
        self.setup_database()

    def setup_database(self):
        try:
            if not os.path.isabs(self.db_path):
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                self.db_path = os.path.normpath(os.path.join(base_dir, self.db_path))
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.conn = duckdb.connect(self.db_path)
            cursor = self.conn.cursor()
            cursor.execute(CARD_TABLE_SCHEMA)
            self.conn.commit()
        except PermissionError as e:
            logger.error(f"Permission error: {e}")
            logger.error(f"Unable to access or create database at {self.db_path}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error setting up database: {e}")
            raise

    def connect(self) -> None:
        logger.debug(f"Connecting to DuckDB at {self.db_path}")
        try:
            self.conn = duckdb.connect(self.db_path)
            logger.debug(f"Connection established to {self.db_path}")
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            if not tables:
                self.conn.execute("DROP TABLE IF EXISTS card")
                self.conn.execute("DROP TABLE IF EXISTS documents")
                self.conn.execute(CARD_TABLE_SCHEMA)
                self.conn.commit()
                logger.debug(f"Database schema created successfully")
                for trigger in TRIGGERS:
                    logger.info(f"Executing SQL: {trigger}")
                    self.conn.execute(trigger)
                    self.conn.commit()
        except Exception as e:
            logger.error(f"Database error connecting to {self.db_path}: {e}")
            raise

    def disconnect(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None

    def commit(self) -> None:
        if self.conn:
            self.conn.commit()

    def rollback(self) -> None:
        if self.conn:
            self.conn.rollback()

class DuckDBEngine(StorageEngine):
    def __init__(self, connection: DuckDBConnection):
        self.connection = connection
        self.connection.connect()

    def __del__(self):
        self.connection.disconnect()

    def add(self, card: MCard) -> str:
        hash_value = str(card.hash)
        try:
            cursor = self.connection.conn.cursor()
            cursor.execute(
                "INSERT INTO card (hash, content, g_time) VALUES (?, ?, ?)",
                (hash_value, card.content, str(card.g_time))
            )
            self.connection.commit()
            logger.debug(f"Added card with hash {hash_value}")
            return hash_value
        except duckdb.ConstraintError:
            raise ValueError(f"Card with hash {hash_value} already exists")

    def get(self, hash_value: str) -> Optional[MCard]:
        cursor = self.connection.conn.cursor()
        cursor.execute("SELECT content, g_time, hash FROM card WHERE hash = ?", (str(hash_value),))
        row = cursor.fetchone()
        if not row:
            return None
        content, g_time, hash = row
        card = MCardFromData(content, hash, g_time)
        return card

    def delete(self, hash_value: str) -> bool:
        cursor = self.connection.conn.cursor()
        cursor.execute("DELETE FROM card WHERE hash = ?", (str(hash_value),))
        self.connection.commit()
        return cursor.rowcount > 0

    def get_page(self, page_number: int = 1, page_size: int = DEFAULT_PAGE_SIZE) -> Page:
        if page_number < 1:
            raise ValueError("Page number must be >= 1")
        if page_size < 1:
            raise ValueError("Page size must be >= 1")
        offset = (page_number - 1) * page_size
        cursor = self.connection.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM card")
        total_items = cursor.fetchone()[0]
        cursor.execute(
            "SELECT content, g_time, hash FROM card ORDER BY g_time DESC LIMIT ? OFFSET ?",
            (page_size, offset)
        )
        items = []
        for row in cursor.fetchall():
            content, g_time, hash = row
            content_bytes = content.encode('utf-8') if isinstance(content, str) else content
            card = MCardFromData(content_bytes, hash, g_time)
            items.append(card)
        return Page(
            items=items,
            total_items=total_items,
            page_number=page_number,
            page_size=page_size,
            has_next=offset + len(items) < total_items,
            has_previous=page_number > 1
        )

    def search_by_string(self, search_string: str, page_number: int = 1, page_size: int = DEFAULT_PAGE_SIZE) -> Page:
        if page_number < 1:
            raise ValueError("Page number must be >= 1")
        if page_size < 1:
            raise ValueError("Page size must be >= 1")
        offset = (page_number - 1) * page_size
        cursor = self.connection.conn.cursor()
        query = """
            SELECT content, g_time, hash FROM card
            WHERE content LIKE ? OR hash LIKE ? OR g_time LIKE ?
            ORDER BY g_time DESC LIMIT ? OFFSET ?
        """
        search_pattern = f"%{search_string}%"
        cursor.execute(query, (search_pattern, search_pattern, search_pattern, page_size, offset))
        items = []
        for row in cursor.fetchall():
            content, g_time, hash = row
            content_bytes = content.encode('utf-8') if isinstance(content, str) else content
            card = MCardFromData(content_bytes, hash, g_time)
            items.append(card)
        cursor.execute("SELECT COUNT(*) FROM card WHERE content LIKE ? OR hash LIKE ? OR g_time LIKE ?", (search_pattern, search_pattern, search_pattern))
        total_items = cursor.fetchone()[0]
        return Page(
            items=items,
            total_items=total_items,
            page_number=page_number,
            page_size=page_size,
            has_next=offset + len(items) < total_items,
            has_previous=page_number > 1
        )

    def search_by_content(self, search_string: str, page_number: int = 1, page_size: int = DEFAULT_PAGE_SIZE) -> Page:
        if page_number < 1:
            raise ValueError("Page number must be >= 1")
        if page_size < 1:
            raise ValueError("Page size must be >= 1")
        offset = (page_number - 1) * page_size
        cursor = self.connection.conn.cursor()
        query = """
            SELECT content, g_time, hash FROM card
            WHERE content LIKE ?
            ORDER BY g_time DESC LIMIT ? OFFSET ?
        """
        search_pattern = f"%{search_string}%"
        cursor.execute(query, (search_pattern, page_size, offset))
        items = []
        for row in cursor.fetchall():
            content, g_time, hash = row
            content_bytes = content.encode('utf-8') if isinstance(content, str) else content
            card = MCardFromData(content_bytes, hash, g_time)
            items.append(card)
        cursor.execute("SELECT COUNT(*) FROM card WHERE content LIKE ?", (search_pattern,))
        total_items = cursor.fetchone()[0]
        return Page(
            items=items,
            total_items=total_items,
            page_number=page_number,
            page_size=page_size,
            has_next=offset + len(items) < total_items,
            has_previous=page_number > 1
        )

    def clear(self):
        cursor = self.connection.conn.cursor()
        cursor.execute("DELETE FROM card")
        self.connection.commit()

    def count(self) -> int:
        cursor = self.connection.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM card")
        return cursor.fetchone()[0]

    def get_all(self, page_number: int = 1, page_size: int = DEFAULT_PAGE_SIZE) -> Page:
        return self.get_page(page_number, page_size)

        offset = (page_number - 1) * page_size
        
        total_items = self.connection.conn.execute(
            "SELECT COUNT(*) FROM card"
        ).fetchone()[0]
        
        results = self.connection.conn.execute(
            "SELECT content, g_time FROM card ORDER BY g_time DESC LIMIT ? OFFSET ?",
            [page_size, offset]
        ).fetchall()
        
        items = [MCard(row[0]) for row in results]
        
        return Page(
            items=items,
            total_items=total_items,
            page_number=page_number,
            page_size=page_size,
            has_next=offset + len(items) < total_items,
            has_previous=page_number > 1
        )
    
    
    def search_by_string(self, search_string: str, page_number: int = 1, page_size: int = 10) -> Page:
        offset = (page_number - 1) * page_size
        search_string = f'%{search_string}%'  # Prepare for LIKE query
        
        cursor = self.connection.conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM card WHERE CAST(hash AS VARCHAR) LIKE ? OR CAST(g_time AS VARCHAR) LIKE ?",
            (search_string, search_string)
        )
        total_items = cursor.fetchone()[0]
        
        cursor.execute(
            "SELECT content, hash, g_time FROM card WHERE CAST(hash AS VARCHAR) LIKE ? OR CAST(g_time AS VARCHAR) LIKE ? ORDER BY g_time DESC LIMIT ? OFFSET ?",
            (search_string, search_string, page_size, offset)
        )
        
        items = [MCard(row[0].decode('utf-8')) for row in cursor.fetchall()]
        
        return Page(
            items=items,
            total_items=total_items,
            page_number=page_number,
            page_size=page_size,
            has_next=offset + len(items) < total_items,
            has_previous=page_number > 1
        )
    
    def clear(self) -> None:
        self.connection.conn.execute("DELETE FROM card")
        self.connection.commit()
    
    def count(self) -> int:
        return self.connection.conn.execute("SELECT COUNT(*) FROM card").fetchone()[0]
