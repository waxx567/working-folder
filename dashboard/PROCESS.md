# The process to get the app to this point

Original brief was to:

Create a billing app for complicated billing.

Decided to make it accessible to all for broader appeal.

Must-haves:
Light and dark mode
Must look good on mobile, tablet and normal size computer screens
Custom colours for the user for a uniue experience
Easier to use than other book-keeping apps and intuitive for those not familiar with online accounting

Nice-to-haves:
Tailored to suit extra-large screens as well

Other names considered:

BILLit

BalanceBooks

Quoll or Quill

Litchi

Quokka

GoodBOOKS (nice name but possibly too close to CookBOOKS)

BrightBOOKS

I didn't know much about accounting and book-keeping so began with several months of learning on the Internet.

Once I was reasonably confident I had some idea, I started by creating these files:

    layout.html - template page for all other html pages to avoid a lot of repetition
    index.html - dashboard for logged in users
    login.html - for users to log in
    register.html - for users to register
    apology.html - if user input is not acceptable
    app.py - python control file that defines routes to the pages
    helpers.py - python file with functions for apology and login_required which are used in most routes in app.py
    requirements.txt - information that may be needed by browsers regarding some packages used by this app

and these tables in a database called books.db

CREATE TABLE person (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
person_id TEXT NOT NULL,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
phone_number TEXT NOT NULL,
email_address TEXT NOT NULL,
);

person is all persons who interact with this business

CREATE TABLE user (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
person_id TEXT NOT NULL,
username TEXT NOT NULL,
hash TEXT NOT NULL,
tier INTEGER NOT NULL,
FOREIGN KEY (person_id) REFERENCES person(person_id)
);

user is all persons who are authorized to use this app

CREATE TABLE employee (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
person_id TEXT NOT NULL,
is_employee BOOLEAN NOT NULL,
FOREIGN KEY (person_id) REFERENCES person(person_id)
);

is employee is either yes (0) or no (1)

originally this person table was these two:

    CREATE TABLE employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    employee_id TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES person(person_id)
    );

    employee is all persons who are employees of this business

    CREATE TABLE contact (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    contact_id TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES person(person_id)
    );

    contact is all persons who are not employees of this business

CREATE TABLE company (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
person_id TEXT NOT NULL,
company_name TEXT NOT NULL,
company_type TEXT NOT NULL,
value_name TEXT NOT NULL,
street TEXT NOT NULL,
city TEXT NOT NULL,
zip_code NUMERIC NOT NULL,
state TEXT NOT NULL,
country TEXT NOT NULL,
phone TEXT NOT NULL,
email TEXT NOT NULL,
terms TEXT NOT NULL,
FOREIGN KEY (person_id) REFERENCES person(person_id)
);

company is for companies the business deals with - customers, suppliers and affiliates - identified by company type eg. CUST, SUPP, AFFL

person id identifies contact person in other organization

CREATE TABLE transactions (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
document_id TEXT NOT NULL,
transaction_date DATE NOT NULL,
due_date DATE NOT NULL,
order_number TEXT NOT NULL,
is_paid BOOLEAN NOT NULL
);

transaction logs all transactions

is paid is either yes (0) or not no (1)

CREATE TABLE income_item (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
document_id TEXT NOT NULL,
sku_code TEXT NOT NULL,
quantity INTEGER NOT NULL,
price DECIMAL(10, 2) NOT NULL,
person_id TEXT NOT NULL,
FOREIGN KEY (sku_code) REFERENCES sku(sku_code),
FOREIGN KEY (person_id) REFERENCES person(person_id)
);

person id identifies which user created each entry

CREATE TABLE expenditure_item (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
document_id TEXT NOT NULL,
sku_code TEXT NOT NULL,
quantity INTEGER NOT NULL,
price DECIMAL(10, 2) NOT NULL,
person_id TEXT NOT NULL,
FOREIGN KEY (sku_code) REFERENCES sku(sku_code),
FOREIGN KEY (person_id) REFERENCES person(person_id)
);

person id identifies which user created each entry

had originally thought to have separate tables for each account type like this:

    CREATE TABLE asset (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    transaction_id INTEGER NOT NULL,
    account_action TEXT NOT NULL,
    allocated_value DECIMAL(10, 2) NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
    );

    CREATE TABLE equity (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    transaction_id INTEGER NOT NULL,
    account_action TEXT NOT NULL,
    allocated_value DECIMAL(10, 2) NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
    );

    CREATE TABLE expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    transaction_id INTEGER NOT NULL,
    account_action TEXT NOT NULL,
    allocated_value DECIMAL(10, 2) NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
    );

    CREATE TABLE liability (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    transaction_id INTEGER NOT NULL,
    account_action TEXT NOT NULL,
    allocated_value DECIMAL(10, 2) NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
    );

    CREATE TABLE revenue (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    transaction_id INTEGER NOT NULL,
    account_action TEXT NOT NULL,
    allocated_value DECIMAL(10, 2) NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
    );

but opted for a single table as it is easier to query and uses far less memory:

CREATE TABLE journal (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
transaction_id INTEGER NOT NULL,
account_name TEXT NOT NULL,
account_type TEXT NOT NULL,
is_debit BOOLEAN NOT NULL,
allocated_value DECIMAL(10, 2) NOT NULL,
person_id INTEGER NOT NULL,
FOREIGN KEY (person_id) REFERENCES person(person_id),
FOREIGN KEY (transaction_id) REFERENCES transactions(id)
);

journal is for values to be allocated to accounts

is debit is either yes ie. debit (0) or no ie. credit (1)

account type is for analysis

transaction id identifies original transaction

person id identifies which user created each entry

CREATE TABLE sku (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
sku_code TEXT NOT NULL,
description TEXT NOT NULL,
quantity INTEGER NOT NULL,
cost_price DECIMAL(10, 2) NOT NULL,
person_id INTEGER NOT NULL,
FOREIGN KEY (person_id) REFERENCES person(person_id)
);

sku is every item the business offers - stock items, service contracts, staff hours charged out, etc.

sku code references all items that can be income or expenditure for this business

cost price is the average purchase price of all items in stock

person id identifies which user created each entry

create the following files:

    invoice.html - to capture transaction information
    income.html - to capture transaction information
    expense.html - to capture transaction information
    expenditure.html - to capture transaction information

list of account names and types to be put into dropdown list when allocating transaction information:

Accounts payable Liability
Accounts receivable Asset
Cash Asset
Dividends Equity
Equipment Asset
Insurance expense Expense
Interest expense Expense
Interest income Revenue
Interest payable Liability
Inventory Asset
Owner’s capital Equity
Real estate Asset
Rent expense Expense
Rental income Revenue
Retained earnings Equity
Salaries and wages Expense
Sales income Revenue
Supplies Asset
Supplies expense Expense
Unearned service revenue Liability
Utilities expense Expense

flow chart can be used for navigation on index (dashboard when logged in) page

Flow chart

Transaction identification
Preparation of voucher or evidence of transaction
Recording of journal entry
Preparation of general ledger
Balancing the ledger
Execution of all adjustments
Preparation of trial balance
Preparation of various financial statements

create the following files:

    accounting.html
    allocation.html
    analysis.html
    transaction.html

still TODO 23/8/2

create books.db
create new tables

app.py / (dashboard)
/transaction
/invoice
/allocation
/balance
/ledger
/accounts
/stock

add business details
add some customers
add some suppliers
add some affiliates

add some skus
add some transactions

still TODO 23/8/3

add business details
where is that going to happen on the app?
doing it in the terminal for now because only employees at a certain tier level would be authorized to complete this action
add some customers
to add customer, first add contact to person and then details to company
where is that going to happen on the app?
doing it in the terminal for now because only employees at a certain tier level would be authorized to complete this action
add some suppliers
same applies
add some affiliates
same applies

add some skus
add some transactions

app.py / (dashboard)
/transaction
/invoice
/allocation
/balance
/ledger
/accounts
/stock

        forms:
            invoice
            purchase order
            receipt

Tables to be redone thusly:

CREATE TABLE person (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
phone_number TEXT NOT NULL,
email_address TEXT NOT NULL,
);

person is basic information on all persons who interact with this business

CREATE TABLE app_user (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
person_id INTEGER NOT NULL,
user_name TEXT NOT NULL,
password_hash TEXT NOT NULL,
FOREIGN KEY (person_id) REFERENCES person(id)
);

app_user is all persons who are authorized to use this app

person id is the identiffier to track all actions undertaken by this user

password hash is an industry standard used to ensure that the password is not visible and remains unknown to anyone but the user

CREATE TABLE status (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
person_id INTEGER NOT NULL,
authorization_level INTEGER NOT NULL,
FOREIGN KEY (person_id) REFERENCES person(id)
);

status is who is allowed to do what

authorization level is the access level for permissions - from 1 (basic permissions) to 5 (all permissions)

CREATE TABLE company (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
person_id INTEGER NOT NULL,
company_name TEXT NOT NULL,
company_type TEXT NOT NULL,
value_name TEXT NOT NULL,
street_address TEXT NOT NULL,
town_or_city TEXT NOT NULL,
zip_code TEXT NOT NULL,
province_state TEXT NOT NULL,
country TEXT NOT NULL,
country_code TEXT NOT NULL,
phone TEXT NOT NULL,
email TEXT NOT NULL,
terms TEXT NOT NULL,
FOREIGN KEY (person_id) REFERENCES person(id)
);

company is for all companies the business deals with - customers, suppliers and affiliates - identified by company type eg. CUST, SUPP, AFFL

person id identifies the contact person within the other organization

searching this table on person id and not getting 0 rows back reveals the person is an employee of the business
1 row means the person is not an employee

CREATE TABLE transactions (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
document_id TEXT NOT NULL,
person_id INTEGER NOT NULL,
transaction_date DATE NOT NULL,
due_date DATE NOT NULL,
order_number TEXT NOT NULL,
is_paid BOOLEAN NOT NULL,
FOREIGN KEY (person_id) REFERENCES person(id)
);

transaction logs all transactions and whether the transaction has been settled one way or the other

is paid is either yes (0) or no (1)

CREATE TABLE sku (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
sku_code TEXT NOT NULL,
item_description TEXT NOT NULL,
quantity INTEGER NOT NULL,
cost_price DECIMAL(10, 2) NOT NULL,
person_id INTEGER NOT NULL,
FOREIGN KEY (person_id) REFERENCES person(person_id)
);

sku is every item the business offers - stock items, service contracts, staff hours charged out, anything and everything etc.

sku code references all items that can be income or expenditure for this business

cost price is the average purchase price of all items in stock

person id identifies which user created each entry

CREATE TABLE income_item (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
document_id TEXT NOT NULL,
sku_code TEXT NOT NULL,
quantity INTEGER NOT NULL,
price DECIMAL(10, 2) NOT NULL,
person_id TEXT NOT NULL,
FOREIGN KEY (document_id) REFERENCES transactions(document_id),
FOREIGN KEY (sku_code) REFERENCES sku(sku_code),
FOREIGN KEY (person_id) REFERENCES person(person_id)
);

person id identifies which user created each entry

CREATE TABLE expenditure_item (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
document_id TEXT NOT NULL,
sku_code TEXT NOT NULL,
quantity INTEGER NOT NULL,
price DECIMAL(10, 2) NOT NULL,
person_id TEXT NOT NULL,
FOREIGN KEY (document_id) REFERENCES transactions(document_id),
FOREIGN KEY (sku_code) REFERENCES sku(sku_code),
FOREIGN KEY (person_id) REFERENCES person(person_id)
);

person id identifies which user created each entry

The code is explained in square brackets underneath like

    [[ this ]]
    [[ Follow the code by looking in the cs50/project/app.py file and reading the comments, as well as reading this square bracket stuff indented under each CAPITALIZED section below. ]]

Just ignore the stuff in the [[square brackets]] if it's confusing. This guide is user-friendly without it.

OPEN APP

Opening the app sees the user on the Login page.
Filling in the details on the Login page correctly and clicking on the button logs the user in. The user will then be redirected to their home page.
There is an option to register displayed in the navigation bar at the top of the screen next to the BrightBOOKS logo. Clicking on Register takes the user to the Register page.
After clicking the submit button, any invalid user input in the fields provided - or if no input is provided - will result in the user being shown the Apology page, which is a picture of a famous Internet cat with a bad-tempered expression and a message steering the user back on track.
The user still has options to click on in the navigation bar to go to either the Login page or the Register page.

    [[ app.route("/") renders the cs50/project/templates/index.html file. The default page of the app. The app will only allow the index page to be rendered after the user has logged in.]]
    [[ When a user is logged in, the program initiates a session and gives the user a session id. @login_required is a function inside cs50/project/helpers.py that searches for a session by checking for a session id. ]]
    [[ The function storing the template for the apology.html page rendering is also in cs50/project/helpers.py. ]]
    [[ If there is no session, @login_required redirects the program to app.route("/register") ]]

REGISTER

The user is asked for details to add the information required to be registered as a user of this app.
Filling in the details on the Register page correctly and clicking on the button stores the user's information and redirect them to the Login page.
Any invalid user input will display the Apology page as detailed above.

    [[ These are the tables - with some explanations below them - as created in the database:

    CREATE TABLE person (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email_address TEXT NOT NULL,
    );

    person is basic information on all persons who interact with this business

    CREATE TABLE app_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    person_id INTEGER NOT NULL,
    user_name TEXT NOT NULL,
    password_hash TEXT NOT NULL
    );

    app_user is all persons who are authorized to use this app

    person id is the identifier to track all actions undertaken by the user with this id number

    password hash is an industry standard used to ensure that the password is saved while not being visible on the app, thus remaining indetectable to anyone else ]]

    [[ app.route("/register") renders the register.html page if the user reached this route via GET (as by clicking a link or via redirect). ]]
    [[ If the user reached this route via POST (as by submitting a form via POST), the information provided by the user is validated first and the cs50/project/templates/apology.html file is rendered if the user inputs incorrectly. ]]
    [[ This GET/POST method of reaching app.routes will be mirrored throughout the app.py file. ]]
    [[ If the user complies, the information is stored in the person and app_user tables in the books.db database.]]
    [[ The program redirects to app.route("/login") ]]

LOGIN
If the user completes the details on the Login page correctly, the user is logged in.
The user will be redirected to his home page.
Any invalid user input will display the Apology page as detailed above
The user still has the options in the navigation bar to go to either the Login or Register pages.

    [[ app.route("/login") renders the cs50/project/templates/login.html page. Information provided by the user is validated first by checking against the app_user table, and the cs50/project/templates/apology.html file is rendered if the user inputs incorrectly. If the user complies, the program redirects to app.route("/") ]]

INDEX
This is the user's home page. A dashboard (**TODO**) shows an overview of the user's activities and other relevant information. The links in the navigation bar now say Transactions and Accounting and the user's name is displayed in red next to the BrightBOOKS logo, signifying that she is logged in.

    [[ app.route("/") renders the cs50/project/templates/index.html page - the html and javascript code for the dashboard charts - now that the login procedure has terminated. The app user table is queried using the session id user name to display the user's name in the navigation bar. Clicking on the navbar links sends the user to the app.routes "/transaction" and "/accounting". Clicking on the dashboard elements (**TODO**) ]]

# 2023/08/03 7:18pm

THE PROBLEMS CAN ONLY BE SOLVED BY HAVING EVERYTHING GO THROUGH THE DASHBOARD

Decision was made to go with a React App Dashboard framework to offer a fully-customizable experience hooking all of the book-keeping components above to that.

Followed along with this video to create the framwork: https://www.youtube.com/watch?v=jx5hdo50a2M

# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)

# 2023/08/05 9:05am

Having too many problems working in the Codespace. Shifting to developing in my local VS Code IDE. Going to start from scratch with the React app. The code can be followed on my github: https://github.com/waxx567 in the fivefiftyfive/dashboard folder

# 2023/08/06 10:12am

Back to local

# 2023/08/07 11:02

Machine giving big probs hanging today. Github Desktop won't open. Going to carry on, but unfortunately this means all future changes are going to end up being saved as one commit, meaning they will be that much more difficult to find.
Going to see if I can commit to GitHub direct from my IDE.

And now the GitHub Desktop is working

1:13pm

Just managed to find an equilibrium where the machine doesn't seem to hang. Hopefully I can finish the setup today. Fingers crossed.

# 2023/08/08 8:30am

Had to delete everything to start all over again. App refused to load for the last four or five hours I was working on it last night. I think it might have been a problem with the machine, but I have no way of knowing. Only option is to start again and be ultra methodical so I just have to go back 1 step if I run into issues. Soldiering on.

10:06am

Cleaned the machine up
