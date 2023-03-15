# The Page Object Model in Practice - Part 1

*Now that we understand a bit about how the Page Object Model pattern is supposed to work, let's begin the work of retooling our test code to use it.*

Let's continue our work with the Page Object Model by moving into some practical examples. I want to start out with the echo box test code we worked with earlier, but first I want to make a new directory called pom for Page Object Model to showcase all the changes we are going to make. But I want to start out with the same test file and the same [<code>conftest.py</code>](https://github.com/lana-20/appium-pom-practice-1/blob/main/pom/conftest.py), so I'll just copy the suite directory and name the new one pom. I can do that on the terminal:

    cp -R suite pom

When I use <code>cp -R</code> on Mac or Linux, it allows me to recursively copy a directory. Of course, you don't need to use the terminal to duplicate this directory; you could use Finder on Mac or the Explorer on Windows. Alright, now I have my [<code>pom</code>](https://github.com/lana-20/appium-pom-practice-1/tree/main/pom) directory, so I'll open it up in the editor, and head over to the [<code>test_echo_box.py</code>](https://github.com/lana-20/appium-pom-practice-1/blob/main/pom/test_echo_box.py) file. Our job is going to be to turn this file into a respectable test file by creating page objects for the views represented here. Let's work on it step by step. What's the view that we are on as we start the test? It's the home view of the app. So let's create a file to represent this view. And I like to keep my page objects organized, so I'm going to create a directory for them all to live in. If I were working with a web app, I'd call this directory <code>pages</code>. Since we're working with a mobile app, I'm going to call it <code>views</code>. Now that I have the [<code>views</code>](https://github.com/lana-20/appium-pom-practice-1/tree/main/pom/views) directory created, I'm going to create a new file called [<code>home_view.py</code>](https://github.com/lana-20/appium-pom-practice-1/blob/main/pom/views/home_view.py). In it I can stub out a page object for this view:

    class HomeView(object):
        pass

Here I'm just creating an empty class that extends the most basic Python object. Now let's go back to our test and ask, what are we doing on the Home view? How is the user intending to use this view? Well, in our case, the only reason for being on the Home view is to get to the Echo Box view. So we can stub out an action in our page object designed to reflect this behavior. We can call it <code>nav_to_echo_box</code>:

        def nav_to_echo_box(self):
                pass

Now we need to implement this method. Let's take a stab at it merely by moving over the implementation details that are already in our test. So I'll take this <code>wait.until</code> line and move it over.

        def nav_to_echo_box(self):
                wait.until(EC.presence_of_element_located(
                    (MobileBy.ACCESSIBILITY_ID, 'Echo Box'))).click()

And this is basically the implementation of <code>nav_to_echo_box</code>. But there are a few things we need to fix before moving on. First, the <code>wait</code> variable is not defined, so let's copy that line over from the other file. I'm just copying and not moving it because the other file still needs the <code>wait</code> as well, and it's nice to keep things working as we make changes.

        def nav_to_echo_box(self):
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located(
                    (MobileBy.ACCESSIBILITY_ID, 'Echo Box'))).click()

This is great, but now we are missing some imports. Our page object file here doesn't know anything about the expected condition class, WebDriverWait, or MobileBy. So let's copy over those imports to the top:

    from appium.webdriver.common.mobileby import MobileBy
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

And we still have one more problem. We're referencing a <code>driver</code> object in constructing our webdriverwait, but we don't have a driver object here. We could pass it in as an argument to this function, but we're going to be using the driver object all throughout each page object we use, so there's a better way: we can pass in the driver object when we construct a page object. To do that, we need to make a constructor function for the class, also known as an initialization method:

        def __init__(self, driver):
                self.driver = driver

In this <code>__init__</code> method, we want to accept a driver object, and then store it locally for reference by other methods. Now that we know we have a driver object as <code>self.driver</code> within any method of this class, we can update our <code>nav_to_echo_box</code> method to use it:

        def nav_to_echo_box(self):
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located(
                    (MobileBy.ACCESSIBILITY_ID, 'Echo Box'))).click()

This looks totally functional now, but there's another practice I recommend following that we'll explore now, which is to keep all the locators at the top of the file or the class, out of the test logic itself. Notice how we define the Echo Box locator using a strategy and a selector tuple. We can just give that tuple a name, and put it up at the top of the class:

    class HomeView(object):
        ECHO_ITEM = (MobileBy.ACCESSIBILITY_ID, 'Echo Box')

Notice I'm putting it outside of any functions, and I'm making it all caps to show that it's a constant. Now we can update our action method once more to use this constant rather than locating it in the action method itself:

        def nav_to_echo_box(self):
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located(self.ECHO_ITEM)).click()

Again, we're doing this both for clean organization and to eliminate any duplication, in case multiple action methods need to make use of the same elements. There's one more step before this is ready, and that is to actually use it! We need to now go back to our [testcase](https://github.com/lana-20/appium-pom-practice-1/blob/main/pom/test_echo_box.py) and use our brand new page object instead of what we had before. So the first thing I need to do of course is to import the page object class up top:

    from views.home_view import HomeView

Here I'm using a Python import that basically says, find the home_view file inside the views directory relative to wherever I'm running Python from, and import the HomeView name from there. Now that we have the name imported, we can use it:

        home = HomeView(driver)
        home.nav_to_echo_box()

Our very first use of our very first page object! This is pretty fun. Our overall test code doesn't look a whole lot prettier yet, but that's because we haven't converted the Echo Box view into an object yet. But before we do that, let's first run this test and make sure it works. It's always good to run things at each stage of a refactor so you don't make too many changes that would be hard to parse apart if something goes wrong. So I can head over to my terminal, navigate into the pom directory, and run the test. This time I'm going to explicitly refer to the test file with the Pytest command, even though it's the only one, so you can see how we would run just one specific test file if we need to:

    pytest test_echo_box.py

This will take a few moments, so while the test is running, let's go ahead and stub out our next page object, which will attempt to model the Echo Box view itself. So I'm going to create a new file called [code>echo_view.py</code>](https://github.com/lana-20/appium-pom-practice-1/blob/main/pom/views/echo_view.py) inside <code>views</code>. And it's probably going to start out looking a lot like <code>home_view.py</code> in terms of its structure, so I'll copy the content from <code>home_view</code> in, and for now I'll simply delete the <code>nav_to_echo_box</code> method, and rename the class itself to <code>EchoView</code>, so all we have are the imports and then a pretty empty class:

    class EchoView(object):

        def __init__(self, driver):
            self.driver = driver

Let's go back and check that our test passed, and yes it did. Excellent. So we can keep on working knowing that the addition of the Home page object didn't mess anything up. Alright back to our Echo View. The first thing we want to ask is, what are the high-level user actions that take place on this view? Well, the most obvious commandment is to save a message. That's the whole point of a view, to enable the user to enter some text which is displayed back to them later on. So let's stub out our first action method:

        def save_message(self, message):
            pass

Notice that we are including a <code>message</code> parameter. We could just hard-code a particular message into this method, but then it wouldn't be generally very useful. A user can type anything they want into this box, and our model should reflect that. It's the test that will be in charge of determining what particular message gets typed, because it's the test that knows what case it is trying to cover. This page object is merely trying to model the potential actions on the page, not say which actions will actually be taken at any given point in time. OK, to implement this method, let's just move the two lines over from the testcase that have to do with typing into the message field and clicking the save button:

        def save_message(self, message):
            wait.until(EC.presence_of_element_located(
                (MobileBy.ACCESSIBILITY_ID, 'messageInput'))).send_keys('Hello')
            driver.find_element(MobileBy.ACCESSIBILITY_ID, 'messageSaveBtn').click()

Now there are a couple things we need to fix. We don't have a wait defined, so our <code>wait</code> variable is a problem. For now, let's copy a wait definition from our other page object, the home view that works. But it is troubling that we are defining waits in multiple places. So let's keep an eye on that to fix it later. And we are also using the <code>driver</code> name here, when that is not a name we have available. Instead, we need to call it <code>self.driver</code>. Finally, we're still sending the string 'Hello' to the <code>send_keys</code> method, rather than using our <code>message</code> parameter, so let's update that as well. OK, those are some good fixes. What's next? Well, we need to pull our element locators up to the top of the class:

        def save_message(self, message):
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located(self.MESSAGE_INPUT)).send_keys('Hello')
            self.driver.find_element(*self.SAVE_BUTTON).click()









