import re
import os
from datetime import datetime
from typing import List, Dict
import pandas as pd

class WhatsAppCollector:
    def __init__(self, export_path=None):
        self.export_path = export_path
        self.messages = []
    
    def parse_whatsapp_export(self, file_path):
        """Parse WhatsApp chat export file"""
        messages = []
        
        # Pattern for WhatsApp messages
        # Format: [DD/MM/YYYY, HH:MM:SS] Contact: Message
        pattern = r'\[(\d{1,2}/\d{1,2}/\d{4}),?\s+(\d{1,2}:\d{2}:\d{2})\]\s+([^:]+):\s+(.*)'
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Find all messages
            matches = re.findall(pattern, content)
            
            for match in matches:
                date_str, time_str, sender, message = match
                
                # Parse datetime
                datetime_str = f"{date_str} {time_str}"
                try:
                    msg_datetime = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M:%S")
                except:
                    try:
                        msg_datetime = datetime.strptime(datetime_str, "%m/%d/%Y %H:%M:%S")
                    except:
                        continue
                
                messages.append({
                    'datetime': msg_datetime,
                    'sender': sender.strip(),
                    'message': message.strip(),
                    'is_customer': not self._is_saved_contact(sender.strip())
                })
                
        except Exception as e:
            print(f"Error parsing WhatsApp export: {e}")
        
        return messages
    
    def _is_saved_contact(self, sender):
        """Check if sender is a saved contact (not a phone number)"""
        # If it's just a phone number, it's likely a customer
        phone_pattern = r'^\+?\d[\d\s\-\(\)]+$'
        return not re.match(phone_pattern, sender)
    
    def get_customer_interactions(self, messages, start_date, end_date):
        """Get customer service interactions within date range"""
        customer_messages = []
        
        for msg in messages:
            if start_date <= msg['datetime'] <= end_date and msg['is_customer']:
                customer_messages.append(msg)
        
        return customer_messages
    
    def analyze_customer_support(self, messages):
        """Analyze customer support activities"""
        analysis = {
            'total_messages': len(messages),
            'unique_customers': len(set(m['sender'] for m in messages if m['is_customer'])),
            'conversations': [],
            'common_topics': {},
            'response_times': []
        }
        
        # Group messages by conversation
        conversations = self._group_conversations(messages)
        
        for conv in conversations:
            conv_data = {
                'customer': conv['customer'],
                'start_time': conv['messages'][0]['datetime'],
                'end_time': conv['messages'][-1]['datetime'],
                'message_count': len(conv['messages']),
                'topics': self._extract_topics(conv['messages'])
            }
            analysis['conversations'].append(conv_data)
        
        # Extract common topics
        all_topics = []
        for conv in analysis['conversations']:
            all_topics.extend(conv['topics'])
        
        for topic in all_topics:
            analysis['common_topics'][topic] = analysis['common_topics'].get(topic, 0) + 1
        
        return analysis
    
    def _group_conversations(self, messages):
        """Group messages into conversations"""
        conversations = []
        current_conv = None
        
        for msg in sorted(messages, key=lambda x: x['datetime']):
            # Start new conversation if it's a different customer or > 2 hours gap
            if current_conv is None or \
               msg['sender'] != current_conv['customer'] or \
               (msg['datetime'] - current_conv['messages'][-1]['datetime']).seconds > 7200:
                
                if current_conv:
                    conversations.append(current_conv)
                
                current_conv = {
                    'customer': msg['sender'],
                    'messages': [msg]
                }
            else:
                current_conv['messages'].append(msg)
        
        if current_conv:
            conversations.append(current_conv)
        
        return conversations
    
    def _extract_topics(self, messages):
        """Extract topics from messages"""
        topics = []
        
        # Keywords for different topics
        topic_keywords = {
            'technical_support': ['error', 'problema', 'no funciona', 'ayuda', 'soporte'],
            'billing': ['factura', 'pago', 'cobro', 'precio', 'costo'],
            'installation': ['instalar', 'instalación', 'configurar', 'setup'],
            'maintenance': ['mantenimiento', 'revisar', 'revisión', 'servicio'],
            'information': ['información', 'consulta', 'pregunta', 'horario'],
            'complaint': ['queja', 'reclamo', 'molesto', 'mal servicio'],
            'appointment': ['cita', 'agendar', 'visita', 'horario']
        }
        
        # Check messages for keywords
        all_text = ' '.join([m['message'].lower() for m in messages])
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                topics.append(topic)
        
        return topics if topics else ['general_inquiry']
    
    def get_statistics(self, start_date, end_date):
        """Get WhatsApp statistics for the period"""
        all_messages = []
        
        # Load all WhatsApp exports
        if self.export_path and os.path.exists(self.export_path):
            if os.path.isfile(self.export_path):
                all_messages = self.parse_whatsapp_export(self.export_path)
            elif os.path.isdir(self.export_path):
                for file in os.listdir(self.export_path):
                    if file.endswith('.txt'):
                        file_path = os.path.join(self.export_path, file)
                        all_messages.extend(self.parse_whatsapp_export(file_path))
        
        # Filter messages by date
        period_messages = [
            m for m in all_messages 
            if start_date <= m['datetime'] <= end_date
        ]
        
        # Get customer interactions
        customer_messages = self.get_customer_interactions(period_messages, start_date, end_date)
        
        # Analyze support activities
        return self.analyze_customer_support(customer_messages)