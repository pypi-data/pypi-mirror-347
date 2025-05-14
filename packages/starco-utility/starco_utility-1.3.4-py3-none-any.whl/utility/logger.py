import logging
from logging.handlers import RotatingFileHandler
import requests
import os,sys
from .file_dir import root_path,directory_creator

class Logger(logging.Logger):
    def __init__(self, name: str, level: int = logging.DEBUG, bot_token: str='7642891094:AAFaKkfCPJQlWyP9orrjaAN9nOz9a5tl6Wc', chat_id: str='1119223961', alert:bool=False,pov:str=None,alert_log_level_inclue:list=None,alert_log_level_exclude:list=None,**kwargs) -> None:
        '''
        log_dir:str=''
        '''
        log_dir=root_path()+'/'+kwargs.get('log_dir',f"/").rstrip('/')
        super().__init__(name, level)
        log_file=f"{log_dir}/{name}.log"
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.alert = alert
         
        self.pov=pov
        self.alert_log_level_inclue=alert_log_level_inclue
        self.alert_log_level_exclude=alert_log_level_exclude
        
        self._formatter = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self._telegram_formatter = kwargs.get('telegram_formatter',"%(name)s - %(levelname)s - %(message)s")
        # Avoid adding duplicate handlers
        if not self.hasHandlers():
            # File handler with rotation
            file_handler = RotatingFileHandler(
                log_file, maxBytes=5 * 1024 * 1024, backupCount=5
            )
            file_handler.setLevel(level)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # Formatter for handlers
            formatter = logging.Formatter(
                self._formatter
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # Add handlers to the logger
            self.addHandler(file_handler)
            self.addHandler(console_handler)

    def send_telegram_message(self, message: str) -> bool:
        """Send message to Telegram if alerting is enabled and credentials are set"""
        if not all([self.alert, self.bot_token, self.chat_id]):
            return False
            
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, data=data)
            return response.status_code == 200
        except Exception as e:
            super().error(f"Failed to send Telegram alert: {str(e)}")
            return False

    def _log_with_telegram(self, level, msg, *args, **kwargs):
        """Internal method to handle logging with Telegram alert"""
        # First, perform normal logging
        # Get correct caller info
        try:
            pathname, lineno, _,_ = self.findCaller()
        except ValueError:
            pathname, lineno, _ = "(unknown file)", 0, "(unknown function)"
        if level not in (logging.ERROR, logging.CRITICAL):
            logMsg=f"(File \"{pathname}\", line {lineno}):\n=>{msg}\n"
        else:logMsg=msg
        super()._log(level, logMsg, args, **kwargs)
        if self.alert_log_level_inclue and level not in self.alert_log_level_inclue:
            return
        if self.alert_log_level_exclude and level in self.alert_log_level_exclude:
            return
        # Then send to Telegram if enabled
        if self.alert and self.bot_token and self.chat_id:
            exc_info = kwargs.get('exc_info', None)
            # Get the caller's frame
            
            
            record = logging.LogRecord(
                name=self.name,
                level=level,
                pathname=pathname,
                lineno=lineno,
                msg=msg,
                args=args,
                exc_info=None
            )
            formatted_msg = logging.Formatter(self._telegram_formatter).format(record)
            level_name = logging.getLevelName(level)
            pov = f"pov={self.pov}\n" if self.pov else ''
        
            # Add traceback for ERROR and CRITICAL levels
            if level in (logging.ERROR, logging.CRITICAL) and exc_info:
                import traceback
                if exc_info is True:
                    exc_info = sys.exc_info()
                if exc_info:
                    tb = ''.join(traceback.format_exception(*exc_info))
                    formatted_msg = f"{formatted_msg}\n\n<pre>{tb}</pre>"
        
            telegram_msg = f"<b>{level_name}</b>\n{pov}{formatted_msg}"
            self.send_telegram_message(telegram_msg)

    def debug(self, msg, *args, **kwargs):
        self._log_with_telegram(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log_with_telegram(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log_with_telegram(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        kwargs.setdefault("exc_info", True)
        self._log_with_telegram(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        kwargs.setdefault("exc_info", True)
        self._log_with_telegram(logging.CRITICAL, msg, *args, **kwargs)
    def debug(self,e):
        self.error(e)
    