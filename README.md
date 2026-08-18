<div align="center">

<img
  src="https://raw.githubusercontent.com/JuliaKeller13/KanMind_frontend/main/assets/icons/logo_icon.svg"
  alt="KanMind Logo"
  width="90"
/>

<h1>KanMind Backend</h1>

<p>
  REST API for collaborative board and task management,<br>
  built with Django and Django REST Framework.
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-6.0.7-092E20?logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-3.17.1-A30000" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/Coverage-100%25-success" alt="Coverage">
  <img src="https://img.shields.io/badge/Lint-Ruff-5A4FCF" alt="Ruff">
</p>

<p>
  <a href="https://github.com/JuliaKeller13/KanMind_frontend">
    <strong>Frontend Repository</strong>
  </a>
  &nbsp;•&nbsp;
  <a href="https://github.com/Developer-Akademie-Backendkurs/project.KanMind">
    Developer Akademie Project
  </a>
</p>

</div>

<hr>

<h2>About</h2>

<p>
  <strong>KanMind</strong> is a collaborative board and task management application.
</p>

<p>
  This repository contains my backend implementation created as part of the
  <strong>Developer Akademie Backend curriculum</strong>.
</p>

<p>
  The REST API provides authentication, boards, tasks, assignments,
  reviews, comments and object-level permissions.
</p>

<blockquote>
  The frontend was originally provided by Developer Akademie.
  I forked and adapted it for integration with this backend.
</blockquote>

<h2>Features</h2>

<table>
  <tr>
    <td align="center" width="25%">
      <img
        src="https://raw.githubusercontent.com/JuliaKeller13/KanMind_frontend/main/assets/icons/login_icon.svg"
        width="30"
        alt="Authentication"
      ><br>
      <strong>Authentication</strong><br>
      Email login & token auth
    </td>
    <td align="center" width="25%">
      <img
        src="https://raw.githubusercontent.com/JuliaKeller13/KanMind_frontend/main/assets/icons/view_board_yellow.svg"
        width="30"
        alt="Boards"
      ><br>
      <strong>Boards</strong><br>
      Owners & members
    </td>
    <td align="center" width="25%">
      <img
        src="https://raw.githubusercontent.com/JuliaKeller13/KanMind_frontend/main/assets/icons/ticket_icon.svg"
        width="30"
        alt="Tasks"
      ><br>
      <strong>Tasks</strong><br>
      Assignment & review
    </td>
    <td align="center" width="25%">
      <img
        src="https://raw.githubusercontent.com/JuliaKeller13/KanMind_frontend/main/assets/icons/comment_bubble_filled.svg"
        width="30"
        alt="Comments"
      ><br>
      <strong>Comments</strong><br>
      Task communication
    </td>
  </tr>
</table>

<ul>
  <li>Custom user model with email-based authentication</li>
  <li>Django REST Framework token authentication</li>
  <li>Board ownership and membership</li>
  <li>Task status, priority, assignee and reviewer workflows</li>
  <li>Personal assigned and reviewing task endpoints</li>
  <li>Task comments with author permissions</li>
  <li>Board task statistics</li>
  <li>Django Admin integration</li>
  <li>100% application-code test coverage</li>
</ul>

<h2>Tech Stack</h2>

<p>
  <strong>Python</strong> •
  <strong>Django</strong> •
  <strong>Django REST Framework</strong> •
  SQLite •
  Token Authentication •
  django-cors-headers •
  python-dotenv •
  Coverage.py •
  Ruff
</p>

<h2>API Overview</h2>

<h3>Authentication</h3>

<table>
  <tr>
    <th>Method</th>
    <th>Endpoint</th>
  </tr>
  <tr>
    <td>POST</td>
    <td><code>/api/registration/</code></td>
  </tr>
  <tr>
    <td>POST</td>
    <td><code>/api/login/</code></td>
  </tr>
</table>

<h3>Boards</h3>

<table>
  <tr>
    <th>Method</th>
    <th>Endpoint</th>
  </tr>
  <tr>
    <td>GET / POST</td>
    <td><code>/api/boards/</code></td>
  </tr>
  <tr>
    <td>GET / PATCH / DELETE</td>
    <td><code>/api/boards/{board_id}/</code></td>
  </tr>
  <tr>
    <td>GET</td>
    <td><code>/api/email-check/</code></td>
  </tr>
</table>

<h3>Tasks</h3>

<table>
  <tr>
    <th>Method</th>
    <th>Endpoint</th>
  </tr>
  <tr>
    <td>POST</td>
    <td><code>/api/tasks/</code></td>
  </tr>
  <tr>
    <td>PATCH / DELETE</td>
    <td><code>/api/tasks/{task_id}/</code></td>
  </tr>
  <tr>
    <td>GET</td>
    <td><code>/api/tasks/assigned-to-me/</code></td>
  </tr>
  <tr>
    <td>GET</td>
    <td><code>/api/tasks/reviewing/</code></td>
  </tr>
</table>

<h3>Comments</h3>

<table>
  <tr>
    <th>Method</th>
    <th>Endpoint</th>
  </tr>
  <tr>
    <td>GET / POST</td>
    <td><code>/api/tasks/{task_id}/comments/</code></td>
  </tr>
  <tr>
    <td>DELETE</td>
    <td><code>/api/tasks/{task_id}/comments/{comment_id}/</code></td>
  </tr>
</table>

<h2>Authentication</h2>

<p>
  Protected endpoints use Django REST Framework Token Authentication.
</p>

<pre><code>Authorization: Token &lt;your-token&gt;</code></pre>

<h2>Setup</h2>

<h3>1. Clone the repository</h3>

<pre><code>git clone https://github.com/JuliaKeller13/Kanmind_backend.git
cd Kanmind_backend</code></pre>

<h3>2. Create and activate a virtual environment</h3>

<h4>Windows PowerShell</h4>

<pre><code>python -m venv .venv
.\.venv\Scripts\Activate.ps1</code></pre>

<h4>macOS / Linux</h4>

<pre><code>python3 -m venv .venv
source .venv/bin/activate</code></pre>

<h3>3. Install dependencies</h3>

<pre><code>python -m pip install -r requirements.txt</code></pre>

<h3>4. Configure the environment</h3>

<p>
  Copy the provided <code>.env.template</code> file:
</p>

<h4>Windows PowerShell</h4>

<pre><code>Copy-Item .env.template .env</code></pre>

<h4>macOS / Linux</h4>

<pre><code>cp .env.template .env</code></pre>

<p>Generate a Django secret key:</p>

<pre><code>python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"</code></pre>

<p>Store it only in your local <code>.env</code>:</p>

<pre><code>SECRET_KEY=your-generated-secret-key</code></pre>

<blockquote>
  <strong>Important:</strong>
  Never commit the real <code>.env</code> file or a real
  <code>SECRET_KEY</code>.
  The committed <code>.env.template</code> contains only a placeholder.
</blockquote>

<h3>5. Prepare the database</h3>

<pre><code>python manage.py migrate</code></pre>

<h3>6. Start the server</h3>

<pre><code>python manage.py runserver</code></pre>

<p>Backend:</p>

<pre><code>http://127.0.0.1:8000/</code></pre>

<h2>Frontend</h2>

<p>
  My adapted frontend fork is available here:
</p>

<p>
  <a href="https://github.com/JuliaKeller13/KanMind_frontend">
    github.com/JuliaKeller13/KanMind_frontend
  </a>
</p>

<p>
  For local development it connects to:
</p>

<pre><code>http://127.0.0.1:8000/api/</code></pre>

<p>
  The original frontend was provided by Developer Akademie:
</p>

<p>
  <a href="https://github.com/Developer-Akademie-Backendkurs/project.KanMind">
    github.com/Developer-Akademie-Backendkurs/project.KanMind
  </a>
</p>

<h2>Testing & Code Quality</h2>

<p>Run all tests:</p>

<pre><code>python manage.py test</code></pre>

<p>Run coverage:</p>

<pre><code>python -m coverage erase
python -m coverage run manage.py test
python -m coverage report -m</code></pre>

<div align="center">

<img
  src="https://img.shields.io/badge/Application%20Coverage-100%25-success"
  alt="100 percent application coverage"
/>

</div>

<p>Run Ruff:</p>

<pre><code>python -m ruff check users_app boards_app tasks_app core --exclude users_app/migrations --exclude boards_app/migrations --exclude tasks_app/migrations</code></pre>

<h2>Project Structure</h2>

<pre>
Kanmind_backend/
├── users_app/
│   ├── api/
│   └── tests/
├── boards_app/
│   ├── api/
│   └── tests/
├── tasks_app/
│   ├── api/
│   └── tests/
├── core/
├── .coveragerc
├── .env.template
├── manage.py
└── requirements.txt
</pre>

<h2>Project Context</h2>

<p>
  KanMind was implemented as a learning project within the
  <strong>Developer Akademie Backend curriculum</strong>.
</p>

<p>
  The frontend was provided as the client application.
  My main task was to design and implement the Django REST API according
  to the project's backend requirements.
</p>

<p>
  This project was used to practice Django architecture, REST APIs,
  relational models, serializers, permissions, authentication,
  validation, automated testing and clean code principles.
</p>

<hr>

<div align="center">

<img
  src="https://raw.githubusercontent.com/JuliaKeller13/KanMind_frontend/main/assets/icons/logo_icon.svg"
  alt="KanMind Logo"
  width="50"
/>

<h3>Julia Keller</h3>

<p>
  <a href="https://github.com/JuliaKeller13">GitHub</a>
  &nbsp;•&nbsp;
  <a href="https://github.com/JuliaKeller13/KanMind_frontend">Frontend</a>
</p>

<p>
  Developed as part of the software development curriculum at
  <strong>Developer Akademie</strong>.
</p>

</div>
