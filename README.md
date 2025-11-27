# Goku vs Gojo Checkers

A checkers game featuring Goku and Gojo as game pieces!

## How to Play

1. Install dependencies: `pip install -r requirements.txt`
2. Run the game: `python checkers.py`

## Controls

- Click a piece to select it (green border)
- Click a yellow dot to move there
- Capture enemy pieces by jumping over them diagonally
- Red (Goku) moves first

## Capture Rules

- **First move is free** - On your first move of the turn, you can choose to capture OR move normally
- **Multi-capture chains** - Once you capture, if the same piece can capture again, it MUST continue capturing
- The piece keeps moving until no more captures are available
- Only after all captures are complete does the turn end
- This gives you strategic choice: capture now or position for a better attack later!

## Power-Up System

### Goku (Red Pieces)
- **Normal**: Kamehameha - Destroys all enemies ahead in the same column
- **Transformation**: Reaches the top row (row 0) → Transforms to Super Saiyan 3 (golden aura)
  - **Transformation Attack**: Throws Genkidama backwards, destroying EVERYTHING in its path (allies and enemies)
- **SSJ3 Powers**: 
  - Can move backward (both directions)
  - Genkidama (Spirit Bomb) - Throws a massive energy ball in the direction of movement, destroys 3x3 area + 2 squares in that direction

### Gojo (Blue Pieces)
- **Normal**: Domain Expansion - Destroys all adjacent enemies (3x3 area)
- **Transformation**: Reaches the bottom row (row 7) → Removes mask (blue aura)
  - **Transformation Attack**: Throws Red and Blue orbs backwards, destroying EVERYTHING in its path (allies and enemies)
- **No Mask Powers**:
  - Can move backward (both directions)
  - Hollow Purple - Red and Blue orbs merge into a purple beam that destroys everything in the direction of movement

## Special Event: ZA WARUDO!

When powered-up Goku (SSJ3) and powered-up Gojo (No Mask) are exactly 2 tiles apart:
- **DIO appears** between them with time-stop animation
- Screen turns green with "ZA WARUDO!" text
- DIO moves randomly to adjacent tiles 3 times
- **Kills anything he touches** (both Goku and Gojo pieces)
- Time resumes and DIO disappears

## Victory Conditions

- **Goku Wins**: Eliminate all Gojo pieces → "GOKU WINS PIBBLERSSSS" with epic orange/gold animations
- **Gojo Wins**: Eliminate all Goku pieces → "GOJO IS BETTER THAN GOKU NERDS" with epic blue/white animations
- Victory screen features:
  - Flashing colored backgrounds
  - Random explosions
  - Pulsing victory text
  - Sparkles and rotating rays
  - 3 seconds of celebration!

## Adding Custom Images

To use custom character images instead of placeholders:

1. Find images of the characters (PNG format recommended):
   - `goku.png` - Base Goku
   - `goku_ssj3.png` - Super Saiyan 3 Goku
   - `gojo.png` - Gojo with mask
   - `gojo_no_mask.png` - Gojo without mask
2. Save them in the same folder as checkers.py
3. Run the game - images will automatically load!

If images are not found, the game uses placeholder circles with text.
