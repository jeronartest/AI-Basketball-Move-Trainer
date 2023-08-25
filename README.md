# Basketball Move Trainer
This is a basketball movement trainer that measures the accuracy of the moves that you do and compares them to other common/famous basketball moves to see how accurate you are.

Install OpenCV

## Basketball Movements

There are basketball movements that you can measure yourself up against.

### Kobe Fade

#### Running w/ WebCam
To run the kobe fade basketball move using your webcam, go to the command prompt and type in the following command:
```
python main.py -mt basketball-move -t kobe-fade
```

#### Running a Video
To run the kobe fade basketball move using a specific video, go to the command prompt/command line, and type in the following command:
```
python main.py -mt basketball-move -t kobe-fade -vs {file-path-to-video}
```
The `{file-path-to-video}` represents where the video exists on your computer. Here is an example of running the kobe-fade using
a pre-set video called `Jeron_Fade.mov`.
```
python main.py -mt basketball-move -t kobe-fade -vs Moves/Jeron_Fade.mov
```

Here is the result of running this video:
![output_jeron_fade.gif](output%2Foutput_jeron_fade.gif)

## Accuracy Calculations

The accuracy is measured at specific times that is dependent on the move that the user is trying to perform.
Example: for the Kobe Fade movement, it's measured at the release point of the fadeaway. The accuracy is then calculated into a score
measuring from 0-100 (0 = not accurate, 100 = highest accuracy).
For additional fun, we decided to make different tiers based on the score. Here are the tiers:
- Him (Score = 80 - 100)
- Goat (Score = 60 - 80)
- Legend (Score = 40 - 60)
- AllStar (Score = 20 - 40)
- League (Score = 1 - 20)
- Bum (Score = 0 - 1)
