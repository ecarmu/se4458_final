import re
from typing import List
from ..schemas.commands import Command, ParsedCommand

class CommandParser:
    def parse_message(self, message: str) -> ParsedCommand:
        """Parse user message and extract commands"""
        message_lower = message.lower()
        commands = []
        
        # Parse search commands
        if any(word in message_lower for word in ['search', 'find', 'look for']):
            commands.append(self._parse_search_command(message))
        
        # Parse apply commands
        if any(word in message_lower for word in ['apply', 'application', 'submit']):
            commands.append(self._parse_apply_command(message))
        
        # Parse filter commands
        if any(word in message_lower for word in ['filter', 'only', 'just']):
            commands.append(self._parse_filter_command(message))
        
        return ParsedCommand(
            original_message=message,
            commands=commands,
            intent=self._determine_intent(message_lower)
        )

    def _parse_search_command(self, message: str) -> Command:
        """Parse search command from message"""
        # Extract job title and location
        job_title = self._extract_job_title(message)
        location = self._extract_location(message)
        
        return Command(
            type="search",
            parameters={
                "job_title": job_title,
                "location": location
            },
            confidence=0.8
        )

    def _parse_apply_command(self, message: str) -> Command:
        """Parse apply command from message"""
        job_id = self._extract_job_id(message)
        
        return Command(
            type="apply",
            parameters={
                "job_id": job_id
            },
            confidence=0.7
        )

    def _parse_filter_command(self, message: str) -> Command:
        """Parse filter command from message"""
        filters = {}
        
        # Extract work mode
        if 'remote' in message.lower():
            filters['work_mode'] = 'remote'
        elif 'hybrid' in message.lower():
            filters['work_mode'] = 'hybrid'
        elif 'on-site' in message.lower():
            filters['work_mode'] = 'on-site'
        
        return Command(
            type="filter",
            parameters=filters,
            confidence=0.6
        )

    def _extract_job_title(self, message: str) -> str:
        """Extract job title from message"""
        # Simple extraction - can be improved with NLP
        words = message.split()
        for i, word in enumerate(words):
            if word.lower() in ['developer', 'engineer', 'manager', 'analyst']:
                return ' '.join(words[max(0, i-2):i+1])
        return ""

    def _extract_location(self, message: str) -> str:
        """Extract location from message"""
        # Simple extraction - can be improved with NLP
        cities = ['istanbul', 'ankara', 'izmir', 'bursa', 'antalya']
        for city in cities:
            if city in message.lower():
                return city.title()
        return ""

    def _extract_job_id(self, message: str) -> str:
        """Extract job ID from message"""
        # Look for patterns like "job #123" or "position 456"
        match = re.search(r'(?:job|position)\s*#?\s*(\d+)', message, re.IGNORECASE)
        return match.group(1) if match else ""

    def _determine_intent(self, message: str) -> str:
        """Determine the main intent of the message"""
        if any(word in message for word in ['search', 'find', 'look for']):
            return 'search'
        elif any(word in message for word in ['apply', 'application']):
            return 'apply'
        elif any(word in message for word in ['filter', 'only']):
            return 'filter'
        else:
            return 'general' 