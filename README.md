<div align="center">

# KanMind Backend

### REST API for collaborative board and task management

<p>
  A Django REST Framework backend developed as a learning project<br>
  within the <strong>Developer Akademie Backend curriculum</strong>.
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-6.0.7-092E20?logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-3.17.1-A30000?logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/Coverage-100%25-success" alt="Coverage">
  <img src="https://img.shields.io/badge/Lint-Ruff-5A4FCF" alt="Ruff">
</p>

<p>
  <a href="https://github.com/JuliaKeller13/Kanmind_backend">
    Backend Repository
  </a>
  &nbsp;•&nbsp;
  <a href="https://github.com/Developer-Akademie-Backendkurs/project.KanMind">
    Provided Frontend
  </a>
</p>

</div>

<hr>

<h2>About the Project</h2>

<p>
  <strong>KanMind</strong> is a collaborative board and task management application.
</p>

<p>
  This repository contains my backend implementation developed during the
  <strong>Developer Akademie Backend course</strong>.
</p>

<p>
  The goal of the project was to build a complete REST API with
  <strong>Django</strong> and <strong>Django REST Framework</strong>
  according to predefined API requirements and connect it to the frontend
  provided by Developer Akademie.
</p>

<blockquote>
  <strong>Project context:</strong><br>
  The frontend was provided by Developer Akademie as part of the learning project.
  This repository contains my own backend implementation.
</blockquote>

<h2>Features</h2>

<table>
  <tr>
    <td>🔐</td>
    <td><strong>Authentication</strong></td>
    <td>Email-based registration and token authentication</td>
  </tr>
  <tr>
    <td>👤</td>
    <td><strong>Custom User Model</strong></td>
    <td>Email is used instead of a username for authentication</td>
  </tr>
  <tr>
    <td>📋</td>
    <td><strong>Boards</strong></td>
    <td>Create, retrieve, update and delete collaborative boards</td>
  </tr>
  <tr>
    <td>👥</td>
    <td><strong>Board Members</strong></td>
    <td>Boards support owners and multiple members</td>
  </tr>
  <tr>
    <td>✅</td>
    <td><strong>Tasks</strong></td>
    <td>Create, assign, review, update and delete tasks</td>
  </tr>
  <tr>
    <td>🔄</td>
    <td><strong>Workflow</strong></td>
    <td>To Do, In Progress, Review and Done task states</td>
  </tr>
  <tr>
    <td>⚡</td>
    <td><strong>Priorities</strong></td>
    <td>Low, Medium and High task priorities</td>
  </tr>
  <tr>
    <td>💬</td>
    <td><strong>Comments</strong></td>
    <td>Create, list and delete comments on tasks</td>
  </tr>
  <tr>
    <td>🛡️</td>
    <td><strong>Permissions</strong></td>
    <td>Authentication and object-level access control</td>
  </tr>
  <tr>
    <td>📊</td>
    <td><strong>Board Statistics</strong></td>
    <td>Task totals, To Do tasks and high-priority task counts</td>
  </tr>
  <tr>
    <td>🧪</td>
    <td><strong>Testing</strong></td>
    <td>Automated tests with 100% application-code coverage</td>
  </tr>
</table>

<h2>Tech Stack</h2>

<table>
  <thead>
    <tr>
      <th>Technology</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Python</td>
      <td>Programming language</td>
    </tr>
    <tr>
      <td>Django 6.0.7</td>
      <td>Backend framework</td>
    </tr>
    <tr>
      <td>Django REST Framework 3.17.1</td>
      <td>REST API</td>
    </tr>
    <tr>
      <td>DRF Token Authentication</td>
      <td>API authentication</td>
    </tr>
    <tr>
      <td>SQLite</td>
      <td>Local development database</td>
    </tr>
    <tr>
      <td>django-cors-headers</td>
      <td>Frontend / backend CORS configuration</td>
    </tr>
    <tr>
      <td>python-dotenv</td>
      <td>Environment variable management</td>
    </tr>
    <tr>
      <td>Coverage.py</td>
      <td>Test coverage</td>
    </tr>
    <tr>
      <td>Ruff</td>
      <td>Python linting</td>
    </tr>
  </tbody>
</table>

<h2>Project Structure</h2>

<pre>
Kanmind_backend/
│
├── boards_app/
│   ├── api/
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── migrations/
│   ├── tests/
│   ├── admin.py
│   ├── apps.py
│   └── models.py
│
├── tasks_app/
│   ├── api/
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── migrations/
│   ├── tests/
│   ├── admin.py
│   ├── apps.py
│   └── models.py
│
├── users_app/
│   ├── api/
│   │   ├── responses.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── migrations/
│   ├── tests/
│   ├── admin.py
│   ├── apps.py
│   ├── managers.py
│   └── models.py
│
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .coveragerc
├── .env.template
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
</pre>

<h2>Installation</h2>

<h3>1. Clone the repository</h3>

<pre><code>git clone https://github.com/JuliaKeller13/Kanmind_backend.git
cd Kanmind_backend</code></pre>

<h3>2. Create a virtual environment</h3>

<h4>Windows PowerShell</h4>

<pre><code>python -m venv .venv
.\.venv\Scripts\Activate.ps1</code></pre>

<h4>macOS / Linux</h4>

<pre><code>python3 -m venv .venv
source .venv/bin/activate</code></pre>

<h3>3. Install dependencies</h3>

<pre><code>python -m pip install -r requirements.txt</code></pre>

<h2>Environment Configuration</h2>

<p>
  Sensitive configuration is not stored directly in the repository.
</p>

<p>
  The repository contains an <code>.env.template</code> file with the
  required environment variable:
</p>

<pre><code>SECRET_KEY=replace-me-with-a-secure-django-secret-key</code></pre>

<h3>Create the local .env file</h3>

<h4>Windows PowerShell</h4>

<pre><code>Copy-Item .env.template .env</code></pre>

<h4>macOS / Linux</h4>

<pre><code>cp .env.template .env</code></pre>

<h3>Generate a Django Secret Key</h3>

<pre><code>python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"</code></pre>

<p>
  Copy the generated value into your local <code>.env</code> file:
</p>

<pre><code>SECRET_KEY=your-generated-secret-key</code></pre>

<blockquote>
  <strong>Important:</strong><br>
  Never commit the real <code>.env</code> file or a real
  <code>SECRET_KEY</code>.<br><br>

  Only <code>.env.template</code> with a placeholder should be committed.
</blockquote>

<p>
  Django loads the key from the environment:
</p>

<pre><code>SECRET_KEY = os.environ["SECRET_KEY"]</code></pre>

<h2>Database Setup</h2>

<p>Apply all migrations:</p>

<pre><code>python manage.py migrate</code></pre>

<p>
  The project uses SQLite for local development.
  The local <code>db.sqlite3</code> file is excluded from version control.
</p>

<h3>Optional: Create an Admin User</h3>

<pre><code>python manage.py createsuperuser</code></pre>

<h2>Run the Development Server</h2>

<pre><code>python manage.py runserver</code></pre>

<p>Backend:</p>

<pre><code>http://127.0.0.1:8000/</code></pre>

<p>Django Admin:</p>

<pre><code>http://127.0.0.1:8000/admin/</code></pre>

<h2>Authentication</h2>

<p>
  KanMind uses <strong>Django REST Framework Token Authentication</strong>.
</p>

<p>
  Registration and login responses contain an authentication token.
  Protected API requests must include:
</p>

<pre><code>Authorization: Token &lt;your-token&gt;</code></pre>

<h2>API Overview</h2>

<h3>Authentication</h3>

<table>
  <thead>
    <tr>
      <th>Method</th>
      <th>Endpoint</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>POST</td>
      <td><code>/api/registration/</code></td>
      <td>Register a new user</td>
    </tr>
    <tr>
      <td>POST</td>
      <td><code>/api/login/</code></td>
      <td>Authenticate a user and return a token</td>
    </tr>
  </tbody>
</table>

<h3>Boards</h3>

<table>
  <thead>
    <tr>
      <th>Method</th>
      <th>Endpoint</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>GET</td>
      <td><code>/api/boards/</code></td>
      <td>Retrieve accessible boards</td>
    </tr>
    <tr>
      <td>POST</td>
      <td><code>/api/boards/</code></td>
      <td>Create a board</td>
    </tr>
    <tr>
      <td>GET</td>
      <td><code>/api/boards/{board_id}/</code></td>
      <td>Retrieve board details including tasks</td>
    </tr>
    <tr>
      <td>PATCH</td>
      <td><code>/api/boards/{board_id}/</code></td>
      <td>Update a board</td>
    </tr>
    <tr>
      <td>DELETE</td>
      <td><code>/api/boards/{board_id}/</code></td>
      <td>Delete a board</td>
    </tr>
    <tr>
      <td>GET</td>
      <td><code>/api/email-check/</code></td>
      <td>Find a user by email address</td>
    </tr>
  </tbody>
</table>

<h3>Tasks</h3>

<table>
  <thead>
    <tr>
      <th>Method</th>
      <th>Endpoint</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>POST</td>
      <td><code>/api/tasks/</code></td>
      <td>Create a new task</td>
    </tr>
    <tr>
      <td>PATCH</td>
      <td><code>/api/tasks/{task_id}/</code></td>
      <td>Update a task</td>
    </tr>
    <tr>
      <td>DELETE</td>
      <td><code>/api/tasks/{task_id}/</code></td>
      <td>Delete a task</td>
    </tr>
    <tr>
      <td>GET</td>
      <td><code>/api/tasks/assigned-to-me/</code></td>
      <td>Retrieve tasks assigned to the authenticated user</td>
    </tr>
    <tr>
      <td>GET</td>
      <td><code>/api/tasks/reviewing/</code></td>
      <td>Retrieve tasks where the authenticated user is reviewer</td>
    </tr>
  </tbody>
</table>

<h4>Supported Task Status Values</h4>

<pre><code>to-do
in-progress
review
done</code></pre>

<h4>Supported Priority Values</h4>

<pre><code>low
medium
high</code></pre>

<h3>Comments</h3>

<table>
  <thead>
    <tr>
      <th>Method</th>
      <th>Endpoint</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>GET</td>
      <td><code>/api/tasks/{task_id}/comments/</code></td>
      <td>Retrieve comments belonging to a task</td>
    </tr>
    <tr>
      <td>POST</td>
      <td><code>/api/tasks/{task_id}/comments/</code></td>
      <td>Create a task comment</td>
    </tr>
    <tr>
      <td>DELETE</td>
      <td><code>/api/tasks/{task_id}/comments/{comment_id}/</code></td>
      <td>Delete a comment</td>
    </tr>
  </tbody>
</table>

<h2>Permissions</h2>

<h3>Boards</h3>

<ul>
  <li>Board owners and members can retrieve board details.</li>
  <li>Only the board owner can update a board.</li>
  <li>Only the board owner can delete a board.</li>
</ul>

<h3>Tasks</h3>

<ul>
  <li>Only board members can create tasks.</li>
  <li>Only board members can edit tasks.</li>
  <li>Assignees must belong to the associated board.</li>
  <li>Reviewers must belong to the associated board.</li>
  <li>Tasks can be deleted by the task creator or board owner.</li>
</ul>

<h3>Comments</h3>

<ul>
  <li>Board members can retrieve comments.</li>
  <li>Board members can create comments.</li>
  <li>Only the comment author can delete their comment.</li>
</ul>

<h2>Testing</h2>

<p>Run the complete Django test suite:</p>

<pre><code>python manage.py test</code></pre>

<p>The automated tests cover:</p>

<ul>
  <li>User management</li>
  <li>Authentication</li>
  <li>Models</li>
  <li>Serializers</li>
  <li>Views</li>
  <li>Permissions</li>
  <li>Boards</li>
  <li>Tasks</li>
  <li>Comments</li>
  <li>Validation</li>
  <li>API error responses</li>
</ul>

<h2>Test Coverage</h2>

<p>
  Coverage is configured through <code>.coveragerc</code>.
</p>

<pre><code>python -m coverage erase
python -m coverage run manage.py test
python -m coverage report -m</code></pre>

<div align="center">

<h3>Application Code Coverage</h3>

<img src="https://img.shields.io/badge/Coverage-100%25-success" alt="100 percent test coverage">

</div>

<p>
  Tests and migrations are excluded from the application-code coverage calculation.
</p>

<h2>Code Quality</h2>

<p>The project uses <strong>Ruff</strong> for linting.</p>

<pre><code>python -m ruff check users_app boards_app tasks_app core --exclude users_app/migrations --exclude boards_app/migrations --exclude tasks_app/migrations</code></pre>

<p>Expected result:</p>

<pre><code>All checks passed!</code></pre>

<h2>Frontend Integration</h2>

<p>
  The frontend for this learning project was provided by
  <strong>Developer Akademie</strong>.
</p>

<p>
  <strong>Frontend Repository:</strong><br>
  <a href="https://github.com/Developer-Akademie-Backendkurs/project.KanMind">
    github.com/Developer-Akademie-Backendkurs/project.KanMind
  </a>
</p>

<p>
  The frontend and backend are maintained as separate repositories.
</p>

<p>
  The backend contains CORS configuration for local frontend development.
</p>

<pre><code>http://127.0.0.1:5500</code></pre>

<h2>Security</h2>

<p>
  Sensitive and local files are excluded from version control.
</p>

<pre><code>.env
db.sqlite3
.venv/
__pycache__/
.coverage
htmlcov/
.ruff_cache/</code></pre>

<p>
  The repository intentionally contains <code>.env.template</code>,
  which documents the required environment variables without exposing
  real credentials.
</p>

<blockquote>
  <strong>Note:</strong>
  <code>DEBUG = True</code> is intended for local development only and
  should be disabled for a production deployment.
</blockquote>

<h2>Project Context</h2>

<p>
  KanMind was developed as part of the
  <strong>Developer Akademie Backend curriculum</strong>.
</p>

<p>
  The project focuses on applying practical backend development concepts,
  including:
</p>

<ul>
  <li>Django project architecture</li>
  <li>Django REST Framework</li>
  <li>RESTful API design</li>
  <li>Custom Django user models</li>
  <li>Token-based authentication</li>
  <li>Relational database modeling</li>
  <li>Serializers and validation</li>
  <li>Object-level permissions</li>
  <li>CRUD operations</li>
  <li>Automated API testing</li>
  <li>Test coverage</li>
  <li>Clean code principles</li>
  <li>Environment variable management</li>
  <li>Git and GitHub workflows</li>
</ul>

<p>
  The frontend was provided by Developer Akademie.
  This repository contains <strong>my backend implementation</strong>
  created according to the project requirements.
</p>

<hr>

<div align="center">

<h2>Author</h2>

<p>
  <strong>Julia Keller</strong>
</p>

<p>
  <a href="https://github.com/JuliaKeller13">
    GitHub Profile
  </a>
  &nbsp;•&nbsp;
  <a href="https://github.com/JuliaKeller13/Kanmind_backend">
    KanMind Backend
  </a>
</p>

<br>

<p>
  Developed as part of the software development curriculum at
  <strong>Developer Akademie</strong>.
</p>

</div>
