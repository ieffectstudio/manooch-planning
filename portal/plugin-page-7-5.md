### Plugin UI Rework Prompt
100% description only. No code logic, no implementation instructions, no technical suggestions. Only describes the existing issue and exact required end behaviour.

***

#### Current Problem
The existing Plugin UI has the following usability issues:
* Plugin cards and the plugin management table are both placed on the same single tab
* Users are forced to scroll all the way past every card to reach the management table to perform any actions
* All edit and delete actions only exist on the table at the very bottom of the page
* The Create New Plugin button is placed in a low visibility location

#### Required Changes
1. Split the Plugin page into two separate distinct tabs at the top of the page:
   * Tab 1: Plugin Cards
   * Tab 2: Plugin Table

2. The plugin management table is no longer required. Remove it entirely from the interface.

3. Add two action buttons directly to every individual plugin card:
   * One Edit button
   * One Delete button

4. Move the Create New Plugin button to the very top of the entire plugin page, above the tabs. It will remain fixed in this position and visible no matter which tab is selected.

#### Required Final Behaviour
* The Cards tab is active by default when a user lands on the plugin page
* A user can toggle between the two tabs at any time
* At no point will a user ever be required to scroll to find any primary action
* All actions for any plugin are available directly on that plugin's card
* There is no remaining requirement for a user to scroll down the page to manage plugins

***

This prompt intentionally excludes all implementation detail. It only tells the developer or AI what the problem is and what the end result should look and behave like, and never tells them how to build it.

If you would like me to adjust any part of this, add extra requirements or refine the behaviour further just let me know.