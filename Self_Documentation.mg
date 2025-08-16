Useful resources 
    - the library documentation (https://ai.google.dev/edge/mediapipe/solutions/guide)
    - youtuber and tutorials (https://www.youtube.com/@Koolac)


log 1 2025/08/12 9:20pm
    - very raw imports and use of code, as of right now it can only track the basic movement, camera is a bit laggy and so i will have to check up on that
    - followed a tutorial for the basic

log 2 2025/08/15 10:14
    - stightly refined code, it functions at a higher frame rate and runs quicker, it still runs off a previously found tutorial online
    - neect step is figuring out wtf to do with this
log 3 2025/08/16
    - added in the ability to track points, currecntly runs basde on whether the tip is close to teh pip (top of finger is above the bottom)
    - issues arrives when you flip the hand in the frame as its "tehcnically above" but the hand isnt closed
    - chaneg from hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y: to a system where teh detects teh proximity "abs( this - that) > 5"