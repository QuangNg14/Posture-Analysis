## **Inspiration**

Since the outbreak of COVID-19, physical education classes across North America and the rest of the world have moved online, making it difficult for so many people to keep up with their fitness. However, this way of practicing PE has been significantly undermined in the context of online gym classes, where learners just follow along as if watching a Youtube video, with little or no feedback from the instructors. The closure of gyms and other fitness activity centers, including sports stadiums, morning walk parks, etc., and the heightened psychological health issues have resulted in the lack of fitness motivation.

In this pursuit of adapting to modern norms, Machine learning concepts are needed to help people with their fitness routine and motivate them to exercise daily. With the help of machine learning, we can estimate the learner’s pose and compare it to the ideal posture to generate an accuracy score that helps the user determine if they are doing the exercises the right way. Even going back to in-person, instructors can take advantage of our tool to provide the most precise feedback for students.

## **What it does**

PostLively.AI shows you different lessons on physical exercises that you can do and how to do them perfectly. There will be a professional instructor for each exercise, and the program will measure how closely you resemble the instructors’ movements and suggest changes. The user can also ask for direct help from the mentor (if the mentor is live) to adjust to the proper pose. We also make a scoreboard for users so we can increase connectivity and competition

## **How we built it**

**Our Data:**

We have two sources of data:

- Yoga Poses Dataset ([Kaggle](https://www.kaggle.com/niharika41298/yoga-poses-dataset)) - Images
- Self captured data (using webcam) - Live feed & Recorded videos

**For Data Science (Machine learning):**

We used Jupyter Notebook to run OpenCV and Mediapipe. Upon running our data in Mediapipe, we were able to get a skeleton map of the body with 33 points. These points can be mapped in 3-dimension as it contains X, Y, and Z axis & visibility. We processed these 132 features (33 points x 4) by saving them into a spreadsheet. Then we divided the spreadsheet into training and testing data.

Using the training set, we were able to create 6 Machine learning models:

- Gradient Boost Classifier
- XGBoost Classifier
- Support Vector Machine
- Logistic Regression
- Ridge Classifier
- Random Forest Classifier

We can make train models by the live view of a webcam or by recorded videos, allowing the instructor (user) to train a machine learning model in their desired pose using their camera

**For Web:**

We build the web interface using Python-Flask, HTML, CSS and Bootstrap. We also use OpenCV to open the webcam and enable recording for the users. Then, we used the videos recorded by the users and pushed the data into our server. After that, we have already set up our Machine Learning model on the server to process the video.

**For Mobile:**

To overcome the scalability issue, we have also designed a mobile app that lets the user use our model with ease. It is built with flutter and will be available for both Android and iOS devices. For authentication purposes we used firebase. For converting the deep learning model for mobile we are making use of the TensorFlow lite library. We are using the model to estimate body poses in real-time and it will guide us whether our pose is correct or not.

## **Challenges we ran into**

- Data collection: getting exercise data with fewer biases
- Time-zone difference: Our team consists of members from 3 countries
- Biases: These can have an effect on the model in real-world tests

## **Accomplishments that we're proud of**

Apart from completing this hack, we were able to collaborate virtually and tackle challenges as a team. We were able to use machine learning to classify different postures. We were able to train a model that has high accuracy (93%) with high precision, recall and f1-score. This showed us our model has fewer false positives and negatives.

## **What we learned**

We learned how to implement the machine learning model in a Python Flask interface. We also learned how to take advantage of OpenCV and Mediapipe to make machine learning models.

## **What's next for PoseLively.AI**

- Implement Ask for Help! Feature: In the case of a live online classroom, the mentor will be notified that a learner is struggling to make the proper pose. The mentor and learner will then be able to give direct and personal advice to the learner on how to improve his or her pose.
- Find a Classroom Feature: This can be useful for beginners who don’t know where to start. They will be directed to take a short survey about their physical conditions and training purposes and preferences, which will be used as information to output suitable classes for that person to enroll into.
- Deploy our app to the Android and IOS platform
- Create a scoreboard to encourage the students and stimulate competition
- Do further training of models, from data collected from professional fitness instructors, possibly by web scraping websites such as BodyBuilding.com
- Do further web development, where teachers/instructors can monitor every student/client in their group, see their progress and how good their posture is.
