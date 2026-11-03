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

## The download rule

**A download button must have a file behind it.** Check the URL returns 200 before the page ships
it. `app-lantern`'s v1.1.0 release existed with **zero assets**, so the Download link went to a
release page with nothing on it — the commonest way a download button lies.

Two habits that stop it:

- build the bundle to a **stable filename** (`dist/lantern.zip`) beside the versioned one, and point
  the page at the stable one — then a version bump never breaks the link;
- a `release.yml` that runs on every `v*` tag, builds the bundle and attaches it, failing the run if
  the zip is missing, too small to be real, or has lost the files the instructions promise.

## Per kind of app

| app | STEP 1 | STEP 2 | STEP 3 |
|---|---|---|---|
| **PWA / web app** | nothing — it is a web page | open the link | *Add to Home Screen* (Share → Add to Home Screen on a phone) |
| **Node app with a launcher** | download the zip, install Node.js — nodejs.org, the green **LTS** button | unzip, double-click **start-…**; the window stays open | type the address it prints on the other device |
| **desktop download** | download the file for Windows or Linux | double-click it — Windows may ask "keep anyway", click **More info → Run anyway** | it opens; nothing else to install |
| **browser extension** | download and unzip the folder | open `chrome://extensions`, turn on **Developer mode**, **Load unpacked**, pick the folder | click the puzzle piece and pin it |
| **a kit (a library)** | copy one file into your project | *(no step — it is one file)* | open the demo page to see what it does |

## The four questions every install block must answer

Learned by writing Lantern's three steps and being asked, immediately:

1. **Where do I get it?** A download button with a file behind it, and what is inside the zip.
2. **How do I add my own content?** The format, a sample to copy, and where the import happens.
3. **How do I configure it?** The two or three settings that exist, named — not "see the docs".
4. **What if it goes wrong?** The three failures a first-timer hits, each with its answer.

A block that stops at "install, run, open" has answered the easiest question and left the reader to
guess the rest.

## Where it applies

Every one of the 96 repos with a landing page. The demo escape line goes in wherever a demo exists;
where there is no demo (a kit, an engine, an `app-no-demo` product) the escape is a screenshot and a
plain sentence about what the thing does.

## Done when

The block is on the page, in the page's own design, and a person who has never opened a terminal can
get from the page to the app running on their own machine without asking anyone a question.
