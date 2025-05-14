from navigator.handlers.types import AppHandler
# Tasker:
from navigator.background import BackgroundQueue
from navigator_auth import AuthHandler
from querysource.services import QuerySource
from parrot.manager import BotManager
from parrot.conf import STATIC_DIR
from parrot.handlers.bots import (
    FeedbackTypeHandler,
    ChatbotFeedbackHandler,
    PromptLibraryManagement,
    ChatbotUsageHandler,
    ChatbotSharingQuestion
)

class Main(AppHandler):
    """
    Main App Handler for Parrot Application.
    """
    app_name: str = 'Parrot'
    enable_static: bool = True
    enable_pgpool: bool = True
    staticdir: str = STATIC_DIR

    def configure(self):
        super(Main, self).configure()
        ### Auth System
        # create a new instance of Auth System
        auth = AuthHandler()
        auth.setup(self.app)
        # Tasker: Background Task Manager:
        tasker = BackgroundQueue(
            app=self.app,
            max_workers=5,
            queue_size=5
        )
        # Loading QUerySource
        qry = QuerySource(
            lazy=False,
            loop=self.event_loop()
        )
        qry.setup(self.app)
        # Chatbot System
        self.bot_manager = BotManager()
        self.bot_manager.setup(self.app)

        # API of feedback types:
        self.app.router.add_view(
            '/api/v1/feedback_types/{feedback_type}',
            FeedbackTypeHandler
        )
        ChatbotFeedbackHandler.configure(self.app, '/api/v1/bot_feedback')
        # Prompt Library:
        PromptLibraryManagement.configure(self.app, '/api/v1/chatbots/prompt_library')
        # Questions (Usage handler, for sharing)
        ChatbotUsageHandler.configure(self.app, '/api/v1/chatbots/usage')
        self.app.router.add_view(
            '/api/v1/chatbots/questions/{sid}',
            ChatbotSharingQuestion
        )


    async def on_prepare(self, request, response):
        """
        on_prepare.
        description: Signal for customize the response while is prepared.
        """

    async def pre_cleanup(self, app):
        """
        pre_cleanup.
        description: Signal for running tasks before on_cleanup/shutdown App.
        """

    async def on_cleanup(self, app):
        """
        on_cleanup.
        description: Signal for customize the response when server is closing
        """

    async def on_startup(self, app):
        """
        on_startup.
        description: Signal for customize the response when server is started
        """
        app['websockets'] = []

    async def on_shutdown(self, app):
        """
        on_shutdown.
        description: Signal for customize the response when server is shutting down
        """
        pass
