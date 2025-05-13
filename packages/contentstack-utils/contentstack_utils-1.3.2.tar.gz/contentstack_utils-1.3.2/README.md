# Contentstack Utility

This guide will help you get started with Contentstack Python Utils SDK to build apps powered by Contentstack.

## Prerequisites

The latest version of [PyCharm](https://www.jetbrains.com/pycharm/download/) or [Visual Studio Code](https://code.visualstudio.com/download)

[Python 3](https://docs.python-guide.org/starting/installation/#python-3-installation-guides)

[Create virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)

[Activate virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment)

## SDK Installation and Setup

To set up Python Utils SDK, Go to terminal and locate the virtual environment path and type below.

```python
   pip install contentstack_utils
```

If you are using Contentstack Python SDK in your project by running the following commands,  then “contentstack_utils”  is already imported into your project.

## For the latest version

```python
   pip install Contentstack
```

## For the specific version

```python
   pip install Contentstack==1.5.1
```

## Usage

Let’s learn how you can use Utils SDK to render embedded items. 

### Create Render Option

To render embedded items on the front-end, use the renderContents function, and define the UI elements you want to show in the front-end of your website, as shown in the example code below:

```python
    from contentstack_utils.utils import Utils
    from contentstack_utils.render.options import Options
    
    json_array = {} # should be type of dictionary or list
    option = Options()
    response = Utils.render_content('html_string', json_array, option)
    print(response)
    
```

## Basic Queries

Contentstack Utils SDK lets you interact with the Content Delivery APIs and retrieve embedded items from the RTE field of an entry.

## Fetch Embedded Item(s) from a Single Entry

To get an embedded item of a single entry, you need to provide the stack API key, environment name, content type’s UID, and entry’s UID. Then, use the `entry.fetch` function as shown below:

```python
import contentstack
    
stack = contentstack.Stack('api_key','delivery_token','environment')
content_type = stack.content_type("content_type_uid")
entry = content_type.entry("entry_uid")
result = entry.fetch()
if result is not None:
   entry = result['entries']
   Utils.render(entry, ['rich_text_editor', 'some_other_text'], Option())
       
```

## Fetch Embedded Item(s) from Multiple Entries

To get embedded items from multiple entries, you need to provide the stack API key, delivery token, environment name, and content type’s UID. 

```python
import contentstack

stack = contentstack.Stack('api_key','delivery_token','environment')
query = stack.content_type("content_type_uid").query()
result = query.find()
if result is not None and 'entries' in result:
   entry = result['entries']
   for item in range:
       option = Option()
       Utils.render(item, ['rich_text_editor', 'some_other_text'], option)
```


## Supercharged

To get supercharged items from multiple entries, you need to provide the stack API key, delivery token, environment name, and content type’s UID. 

```python
import contentstack

stack = contentstack.Stack('api_key','delivery_token','environment')
query = stack.content_type("content_type_uid").query()
result = query.find()
if result is not None and 'entries' in result:
   entry = result['entries']
   for item in entry:
       option = Option()
       Utils.json_to_html(item, ['paragraph_text'], option)
```

## GraphQL SRTE

To get supercharged items from multiple entries, you need to provide the stack API key, delivery token, environment name, and content type’s UID. 

```python
import contentstack

stack = contentstack.Stack('api_key','delivery_token','environment')
query = stack.content_type("content_type_uid").query()
result = query.find()
if result is not None and 'entries' in result:
   entry = result['entries']
   for item in entry:
       option = Option()
       GQL.json_to_html(item, ['paragraph_text'], option)
```
