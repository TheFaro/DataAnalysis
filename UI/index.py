# local module imports
import menu as menu
import app as App  # local module that has the menu definition root


# This is the start of the main function
if __name__ == "__main__":
    app = App.App()
    app.title('Data Collecting and Chart Viewer Tool')
    menu.makemenu(app)
    app.mainloop()
