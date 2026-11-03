# The install block: instructions for the person who will actually use it

Lantern is for a school, a clinic, a village. Its page told them to type `node server.js` into a
terminal. That is not an instruction, it is a password.

The rule, for every landing page in the estate:

> **If the first step is a command, the block has failed.** The reader is not the person who built
> it. Write for someone who has never opened a terminal, and put the terminal underneath for the
> people who want it.

## The test

Read the block as the least technical person who could plausibly want the app — a teacher with a
laptop, a shopkeeper with a phone. Then ask:

- Can they do step 1 without knowing what a "runtime", a "dependency" or a "build step" is?
- Does every step name the thing they will actually see on screen — a button, a window, an address?
- If a step needs a program installed first, does it say so, and say where to get it in one line?
- Is there a way to try the thing **without installing anything**, offered first?

A block that passes all four is done.

## The shape

Three cards, the page's own `.three` / `.card` / `.num` classes. Not a numbered list of eight steps:
three is the most a person will hold in their head.

| | |
|---|---|
| **STEP 1** | the one thing to install, with the exact button to click |
| **STEP 2** | the one action that starts it, named as they will see it (double-click **start-lantern**) |
| **STEP 3** | what they do next, in the words they will use ("type the address into your phone") |

Then one `.hint` line carrying the escape hatch and the terminal:

> Would rather not install anything yet? **Open the demo** — the real app, running over a sample
> library. Already live in a terminal? The whole thing is `node server.js`.

## The vocabulary

Every one of these has cost a real person an install.

| never say | say |
|---|---|
| run the server / `node server.js` | double-click **start-lantern** |
| install dependencies | *(nothing — a plain-language install has no dependencies)* |
| `localhost:8080` | an address like `http://192.168.1.24:8080/` |
| clone the repository | download the file |
| build step / compile | *(delete the sentence)* |
| runtime, binary, daemon | the program |
| PWA / service worker | add it to your home screen |
| side-load / unpacked extension | load it into your browser once |
| Raspberry Pi, headless | a small computer |

## The launcher rule

**If the copy says "double-click", the repo must ship the double-clickable file.** The copy is not
allowed to promise a step that does not exist — that is how the jargon got there in the first place:
there was no launcher, so the only true instruction was the command.

`app-lantern` now ships `start-lantern.bat` and `start-lantern.sh`. Both find `lantern.js` or
`server.js`, say plainly what to do when Node is missing, and open the browser. The page promises
exactly what the repo delivers.

## Per kind of app

| app | STEP 1 | STEP 2 | STEP 3 |
|---|---|---|---|
| **PWA / web app** | nothing — it is a web page | open the link | *Add to Home Screen* (Share → Add to Home Screen on a phone) |
| **Node app with a launcher** | install Node.js — nodejs.org, the green **LTS** button | double-click **start-…**; the window stays open | type the address it prints on the other device |
| **desktop download** | download the file for Windows or Linux | double-click it — Windows may ask "keep anyway", click **More info → Run anyway** | it opens; nothing else to install |
| **browser extension** | download and unzip the folder | open `chrome://extensions`, turn on **Developer mode**, **Load unpacked**, pick the folder | click the puzzle piece and pin it |
| **a kit (a library)** | copy one file into your project | *(no step — it is one file)* | open the demo page to see what it does |

## Where it applies

Every one of the 96 repos with a landing page. The demo escape line goes in wherever a demo exists;
where there is no demo (a kit, an engine, an `app-no-demo` product) the escape is a screenshot and a
plain sentence about what the thing does.

## Done when

The block is on the page, in the page's own design, and a person who has never opened a terminal can
get from the page to the app running on their own machine without asking anyone a question.
