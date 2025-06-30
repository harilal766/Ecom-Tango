# Installation and running
1. **Clone the Repository** : ```git clone "https://github.com/harilal766/Ecom-Tango"```
2. **Create a Virtual Environment** : ```python -m venv env```
3. **Activate the Virtual Environment** : ```env/scripts/activate```
4. **Install Dependencies**: : ```pip install -r requirements.txt```

5. **Set Up the Database**:

   - Ensure PostgreSQL is installed and running (or use SQLite for development).
   - Update the `DATABASES` setting in `Ecom-Tango/settings.py` with your database configuration. Example for sqlite:

     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.sqlite',
             'NAME': 'ecom_tango_db',
             'USER': 'your_username',
             'PASSWORD': 'your_password',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```
   - Run migrations:

     ```bash
     python manage.py migrate
     ```

6. **Run the Development Server**:

   ```bash 
   python manage.py runserver
   ```

   Access the application at `http://localhost:8000`.