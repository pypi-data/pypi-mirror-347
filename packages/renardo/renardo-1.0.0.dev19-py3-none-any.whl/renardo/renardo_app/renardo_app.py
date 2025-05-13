"""
RenardoApp - Main application class for Renardo
"""
import argparse
import time

from renardo.sc_backend import write_sc_renardo_files_in_user_config
from renardo.webserver import create_webapp
from renardo.webserver.config import HOST, PORT, DEBUG

from .state_manager import StateManager


class RenardoApp:
    """
    Main application class for Renardo
    """
    _instance = None  # Singleton instance
    
    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance"""
        if cls._instance is None:
            cls._instance = RenardoApp()
        return cls._instance
    
    def __init__(self):
        """Initialize the Renardo application"""
        # Ensure only one instance is created
        if RenardoApp._instance is not None:
            raise RuntimeError("RenardoApp is a singleton class. Use RenardoApp.get_instance() instead.")
            
        # Create state manager
        self.state_manager = StateManager()
        
        # Flask webapp instance
        self.webapp = None
        
        # Parse arguments
        self.args = self.parse_args()
        
        # Set singleton instance
        RenardoApp._instance = self
    
    def launch(self):
        """Launch the Renardo application"""
        # Handle command-line options
        if self.args.create_scfiles:
            write_sc_renardo_files_in_user_config()
            
            # Update the state
            self.state_manager.update_renardo_init_status("superColliderClasses", True)

        # Create and launch web server if not using pipe or foxdot editor
        if not (self.args.pipe or self.args.foxdot_editor):
            # Create the Flask application if it doesn't exist
            webapp = self.create_webapp_instance()
            
            # Run the web server with Gunicorn or Flask development server
            if self.args.use_gunicorn:
                self._run_with_gunicorn()
            else:
                # Run the Flask application (development server)
                webapp.run(
                    host=HOST,
                    port=PORT,
                    debug=DEBUG
                )
        # Handle different run modes
        elif self.args.pipe:
            from renardo.lib.runtime import handle_stdin, FoxDotCode
            # Just take commands from the CLI
            handle_stdin()
        elif self.args.foxdot_editor:
            from renardo.lib.runtime import FoxDotCode
            # Open the GUI
            from renardo.foxdot_editor.Editor import workspace
            FoxDot = workspace(FoxDotCode).run()
        elif self.args.no_tui:
            print("You need to choose a launching mode: TUI, --pipe or --foxdot-editor...")
        
        print("Quitting...")
        
    def _run_with_gunicorn(self):
        """Run the web application with Gunicorn"""
        import subprocess
        import sys
        import os
        import importlib.util
        from pathlib import Path
        
        try:
            # Import gunicorn to verify it's installed
            import gunicorn
            import gevent
        except ImportError as e:
            print(f"Error: Missing dependency: {e}")
            print("Please install required packages with: pip install gunicorn gevent")
            sys.exit(1)
            
        # Get path to the webserver module
        from renardo import webserver
        webserver_path = Path(webserver.__file__).parent
        
        # Get the path to the gunicorn config
        gunicorn_config = webserver_path / "gunicorn_config.py"
        
        # Get the path to the WSGI module
        wsgi_module = "renardo.webserver.wsgi:app"
        
        print(f"Starting Gunicorn server at {HOST}:{PORT}...")
        
        # Instead of running Gunicorn as a separate process, we'll invoke it through its API
        # This avoids the command-line argument parsing issue
        try:
            # Import the necessary module
            from gunicorn.app.wsgiapp import WSGIApplication
            
            # Create a custom WSGI application class that loads our config
            class RenardoWSGIApplication(WSGIApplication):
                def __init__(self, config_path):
                    self.config_path = config_path
                    super().__init__()
                
                def load_config(self):
                    # Load the config file first
                    config_path = self.config_path
                    
                    # Check if file exists
                    if not os.path.exists(config_path):
                        print(f"Error: Config file not found: {config_path}")
                        sys.exit(1)
                    
                    # Load the module
                    spec = importlib.util.spec_from_file_location("gunicorn_config", config_path)
                    config_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(config_module)
                    
                    # Load settings from the module
                    for key in dir(config_module):
                        if key.isupper():
                            continue
                            
                        # Skip internal attributes and functions
                        if key.startswith('__'):
                            continue
                            
                        value = getattr(config_module, key)
                        if callable(value) or value is None:
                            continue
                            
                        self.cfg.set(key, value)
                    
                    # Add our application module
                    self.app_uri = wsgi_module
            
            # Initialize and run the Gunicorn application
            gunicorn_app = RenardoWSGIApplication(str(gunicorn_config))
            gunicorn_app.run()
            
        except Exception as e:
            print(f"Error starting Gunicorn: {e}")
            # Fallback to subprocess method if the direct invocation fails
            print("Falling back to subprocess method...")
            
            # Use Python to explicitly run the process to avoid argument parsing issues
            python_executable = sys.executable
            cmd = [
                python_executable,
                "-m", "gunicorn.app.wsgiapp",
                "--config", str(gunicorn_config),
                wsgi_module
            ]
            
            # Run gunicorn
            process = subprocess.Popen(cmd)
            
            try:
                # Wait for gunicorn to exit
                process.wait()
            except KeyboardInterrupt:
                print("\nShutting down Gunicorn...")
                process.terminate()
                process.wait()

    def create_webapp_instance(self):
        """
        Create the Flask webapp instance if it doesn't exist
        
        Returns:
            Flask: The Flask webapp instance
        """
        if self.webapp is None:
            self.webapp = create_webapp()
        return self.webapp
        
    @staticmethod
    def parse_args():
        """Parse command-line arguments"""
        parser = argparse.ArgumentParser(
            prog="renardo",
            description="Live coding with Python and SuperCollider",
            epilog="More information: https://renardo.org/"
        )
        parser.add_argument('-p', '--pipe', action='store_true', help="run Renardo from the command line interface")
        parser.add_argument('-f', '--foxdot-editor', action='store_true', help="run Renardo with the classic FoxDot code editor")
        parser.add_argument('-c', '--create-scfiles', action='store_true', help="Create Renardo class file and startup file in SuperCollider user conf dir.")
        parser.add_argument('-N', '--no-tui', action='store_true', help="Don't start Renardo TUI")
        parser.add_argument('-g', '--use-gunicorn', action='store_true', help="Use Gunicorn to serve the web application (1 process, 10 threads)")

        return parser.parse_args()