from src.gui.main_window import MainWindow
from src.business.concurrent import BackgroundWorker, AutoSaveTask, StatisticsTask
from config import AUTO_SAVE_INTERVAL, STATS_RECALC_INTERVAL


class MainWindowWithAsync(MainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.background_worker = BackgroundWorker(
            interval=1,
            name="FinanceTrackerWorker"
        )
        
        # Registriraj zadatke
        self.background_worker.add_task(
            AutoSaveTask(self.manager, AUTO_SAVE_INTERVAL)
        )
        self.background_worker.add_task(
            StatisticsTask(self.manager, STATS_RECALC_INTERVAL)
        )
        
        # Pokreni
        self.background_worker.start()
        
        # Registriraj za čišćenje pri zatvaranju
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    # Zatvori aplikaciju i zaustavi background
    def _on_closing(self) -> None:
        self.background_worker.stop()
        self.destroy()
