# The Page Object Model in Practice - Part 1

*Now that we understand a bit about how the Page Object Model pattern is supposed to work, let's begin the work of retooling our test code to use it.*

Let's continue our work with the Page Object Model by moving into some practical examples. I want to start out with the echo box test code we worked with earlier, but first I want to make a new directory called pom for Page Object Model to showcase all the changes we are going to make. But I want to start out with the same test file and the same [<code>conftest.py</code>](https://github.com/lana-20/appium-pom-practice-1/blob/main/pom/conftest.py), so I'll just copy the suite directory and name the new one pom. I can do that on the terminal:

    cp -R suite pom

When I use <code>cp -R</code> on Mac or Linux, it allows me to recursively copy a directory. Of course, you don't need to use the terminal to duplicate this directory; you could use Finder on Mac or the Explorer on Windows. Alright, now I have my [<code>pom</code>](https://github.com/lana-20/appium-pom-practice-1/tree/main/pom) directory, so I'll open it up in the editor, and head over to the [<code>test_echo_box.py</code>](https://github.com/lana-20/appium-pom-practice-1/blob/main/pom/test_echo_box.py) file. Our job is going to be to turn this file into a respectable test file by creating page objects for the views represented here. Let's work on it step by step. What's the view that we are on as we start the test? It's the home view of the app. So let's create a file to represent this view. And I like to keep my page objects organized, so I'm going to create a directory for them all to live in. If I were working with a web app, I'd call this directory <code>pages</code>. Since we're working with a mobile app, I'm going to call it <code>views</code>. Now that I have the [<code>views</code>](https://github.com/lana-20/appium-pom-practice-1/tree/main/pom/views) directory created, I'm going to create a new file called <code>home_view.py</code>. In it I can stub out a page object for this view:

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







