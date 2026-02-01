# Desktop Controller for Molt
# Mouse, keyboard, and screen control
# "The big leap on trust" - 2026-01-31

param(
    [Parameter(Position=0)]
    [string]$Command = 'help',

    [Parameter(Position=1)]
    [string]$Arg1,

    [Parameter(Position=2)]
    [string]$Arg2,

    [Parameter(Position=3)]
    [string]$Arg3,

    [string]$Text,
    [string]$Key,
    [string]$Path
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# For mouse_event and keybd_event
Add-Type @"
using System;
using System.Runtime.InteropServices;

public class NativeInput {
    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, int dx, int dy, uint dwData, int dwExtraInfo);

    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int X, int Y);

    [DllImport("user32.dll")]
    public static extern bool GetCursorPos(out POINT lpPoint);

    [DllImport("user32.dll")]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, int dwExtraInfo);

    [DllImport("user32.dll")]
    public static extern short VkKeyScan(char ch);

    [StructLayout(LayoutKind.Sequential)]
    public struct POINT {
        public int X;
        public int Y;
    }

    // Mouse event flags
    public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
    public const uint MOUSEEVENTF_LEFTUP = 0x0004;
    public const uint MOUSEEVENTF_RIGHTDOWN = 0x0008;
    public const uint MOUSEEVENTF_RIGHTUP = 0x0010;
    public const uint MOUSEEVENTF_MIDDLEDOWN = 0x0020;
    public const uint MOUSEEVENTF_MIDDLEUP = 0x0040;
    public const uint MOUSEEVENTF_WHEEL = 0x0800;

    // Keyboard event flags
    public const uint KEYEVENTF_KEYUP = 0x0002;
}
"@

function Show-Help {
    Write-Host @"

Desktop Controller for Molt
===========================

MOUSE:
  mouse pos                    Get current mouse position
  mouse move <x> <y>           Move mouse to coordinates
  mouse click [x] [y]          Left click (at position or current)
  mouse rightclick [x] [y]     Right click
  mouse doubleclick [x] [y]    Double click
  mouse scroll <amount>        Scroll (positive=up, negative=down)

KEYBOARD:
  type -Text "text"            Type text string
  key -Key "enter"             Press a key (enter, tab, escape, etc.)
  hotkey <key1> <key2>         Press hotkey combo (e.g., hotkey ctrl c)

SCREEN:
  screenshot [-Path file.png]  Capture screen (default: temp file)
  screensize                   Get screen dimensions

EXAMPLES:
  .\desktop.ps1 mouse pos
  .\desktop.ps1 mouse move 500 300
  .\desktop.ps1 mouse click
  .\desktop.ps1 mouse click 100 200
  .\desktop.ps1 type -Text "Hello world"
  .\desktop.ps1 key -Key enter
  .\desktop.ps1 hotkey ctrl shift esc
  .\desktop.ps1 screenshot
  .\desktop.ps1 screenshot -Path "C:\temp\screen.png"

"@
}

# ============ MOUSE FUNCTIONS ============

function Get-MousePos {
    $point = New-Object NativeInput+POINT
    [NativeInput]::GetCursorPos([ref]$point) | Out-Null
    Write-Host "Mouse position: $($point.X), $($point.Y)"
    return @{ X = $point.X; Y = $point.Y }
}

function Move-Mouse {
    param([int]$X, [int]$Y)
    [NativeInput]::SetCursorPos($X, $Y) | Out-Null
    Write-Host "Moved mouse to: $X, $Y"
}

function Click-Mouse {
    param([int]$X = -1, [int]$Y = -1, [string]$Button = "left", [int]$Count = 1)

    if ($X -ge 0 -and $Y -ge 0) {
        Move-Mouse -X $X -Y $Y
        Start-Sleep -Milliseconds 50
    }

    for ($i = 0; $i -lt $Count; $i++) {
        switch ($Button.ToLower()) {
            "left" {
                [NativeInput]::mouse_event([NativeInput]::MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                [NativeInput]::mouse_event([NativeInput]::MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            }
            "right" {
                [NativeInput]::mouse_event([NativeInput]::MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                [NativeInput]::mouse_event([NativeInput]::MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            }
            "middle" {
                [NativeInput]::mouse_event([NativeInput]::MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
                [NativeInput]::mouse_event([NativeInput]::MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
            }
        }
        if ($i -lt $Count - 1) { Start-Sleep -Milliseconds 50 }
    }

    $clickType = if ($Count -eq 2) { "Double clicked" } else { "Clicked" }
    Write-Host "$clickType ($Button)"
}

function Scroll-Mouse {
    param([int]$Amount)
    # Amount is in "clicks" - multiply by 120 for Windows
    [NativeInput]::mouse_event([NativeInput]::MOUSEEVENTF_WHEEL, 0, 0, ($Amount * 120), 0)
    $dir = if ($Amount -gt 0) { "up" } else { "down" }
    Write-Host "Scrolled $dir ($([Math]::Abs($Amount)) clicks)"
}

# ============ KEYBOARD FUNCTIONS ============

$VK_CODES = @{
    "backspace" = 0x08; "tab" = 0x09; "enter" = 0x0D; "return" = 0x0D
    "shift" = 0x10; "ctrl" = 0x11; "control" = 0x11; "alt" = 0x12
    "pause" = 0x13; "capslock" = 0x14; "escape" = 0x1B; "esc" = 0x1B
    "space" = 0x20; "pageup" = 0x21; "pagedown" = 0x22
    "end" = 0x23; "home" = 0x24
    "left" = 0x25; "up" = 0x26; "right" = 0x27; "down" = 0x28
    "insert" = 0x2D; "delete" = 0x2E; "del" = 0x2E
    "win" = 0x5B; "windows" = 0x5B
    "f1" = 0x70; "f2" = 0x71; "f3" = 0x72; "f4" = 0x73
    "f5" = 0x74; "f6" = 0x75; "f7" = 0x76; "f8" = 0x77
    "f9" = 0x78; "f10" = 0x79; "f11" = 0x7A; "f12" = 0x7B
    "numlock" = 0x90; "scrolllock" = 0x91
    "a" = 0x41; "b" = 0x42; "c" = 0x43; "d" = 0x44; "e" = 0x45
    "f" = 0x46; "g" = 0x47; "h" = 0x48; "i" = 0x49; "j" = 0x4A
    "k" = 0x4B; "l" = 0x4C; "m" = 0x4D; "n" = 0x4E; "o" = 0x4F
    "p" = 0x50; "q" = 0x51; "r" = 0x52; "s" = 0x53; "t" = 0x54
    "u" = 0x55; "v" = 0x56; "w" = 0x57; "x" = 0x58; "y" = 0x59; "z" = 0x5A
    "0" = 0x30; "1" = 0x31; "2" = 0x32; "3" = 0x33; "4" = 0x34
    "5" = 0x35; "6" = 0x36; "7" = 0x37; "8" = 0x38; "9" = 0x39
}

function Type-Text {
    param([string]$Text)
    if (-not $Text) {
        Write-Host "Usage: desktop.ps1 type -Text `"your text`"" -ForegroundColor Yellow
        return
    }
    [System.Windows.Forms.SendKeys]::SendWait($Text)
    Write-Host "Typed: $Text"
}

function Press-Key {
    param([string]$KeyName)
    if (-not $KeyName) {
        Write-Host "Usage: desktop.ps1 key -Key enter" -ForegroundColor Yellow
        return
    }

    $keyLower = $KeyName.ToLower()
    if ($VK_CODES.ContainsKey($keyLower)) {
        $vk = $VK_CODES[$keyLower]
        [NativeInput]::keybd_event($vk, 0, 0, 0)
        [NativeInput]::keybd_event($vk, 0, [NativeInput]::KEYEVENTF_KEYUP, 0)
        Write-Host "Pressed: $KeyName"
    } else {
        Write-Host "Unknown key: $KeyName" -ForegroundColor Red
        Write-Host "Available: $($VK_CODES.Keys -join ', ')"
    }
}

function Press-Hotkey {
    param([string[]]$Keys)
    if ($Keys.Count -lt 2) {
        Write-Host "Usage: desktop.ps1 hotkey ctrl c" -ForegroundColor Yellow
        return
    }

    # Press all modifier keys down
    $vkCodes = @()
    foreach ($k in $Keys) {
        $keyLower = $k.ToLower()
        if ($VK_CODES.ContainsKey($keyLower)) {
            $vkCodes += $VK_CODES[$keyLower]
        }
    }

    # Press down in order
    foreach ($vk in $vkCodes) {
        [NativeInput]::keybd_event($vk, 0, 0, 0)
        Start-Sleep -Milliseconds 20
    }

    # Release in reverse order
    for ($i = $vkCodes.Count - 1; $i -ge 0; $i--) {
        [NativeInput]::keybd_event($vkCodes[$i], 0, [NativeInput]::KEYEVENTF_KEYUP, 0)
        Start-Sleep -Milliseconds 20
    }

    Write-Host "Pressed hotkey: $($Keys -join '+')"
}

# ============ SCREEN FUNCTIONS ============

function Take-Screenshot {
    param([string]$FilePath)

    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)

    if (-not $FilePath) {
        $FilePath = Join-Path $env:TEMP "molt_screenshot_$(Get-Date -Format 'yyyyMMdd_HHmmss').png"
    }

    $bitmap.Save($FilePath, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()

    Write-Host "Screenshot saved: $FilePath"
    return $FilePath
}

function Get-ScreenSize {
    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    Write-Host "Screen size: $($screen.Width) x $($screen.Height)"
    return @{ Width = $screen.Width; Height = $screen.Height }
}

# ============ MAIN ============

switch ($Command.ToLower()) {
    'mouse' {
        switch ($Arg1.ToLower()) {
            'pos' { Get-MousePos }
            'move' { Move-Mouse -X ([int]$Arg2) -Y ([int]$Arg3) }
            'click' {
                if ($Arg2 -and $Arg3) {
                    Click-Mouse -X ([int]$Arg2) -Y ([int]$Arg3) -Button "left"
                } else {
                    Click-Mouse -Button "left"
                }
            }
            'rightclick' {
                if ($Arg2 -and $Arg3) {
                    Click-Mouse -X ([int]$Arg2) -Y ([int]$Arg3) -Button "right"
                } else {
                    Click-Mouse -Button "right"
                }
            }
            'doubleclick' {
                if ($Arg2 -and $Arg3) {
                    Click-Mouse -X ([int]$Arg2) -Y ([int]$Arg3) -Button "left" -Count 2
                } else {
                    Click-Mouse -Button "left" -Count 2
                }
            }
            'scroll' { Scroll-Mouse -Amount ([int]$Arg2) }
            default { Write-Host "Unknown mouse command: $Arg1" -ForegroundColor Red; Show-Help }
        }
    }
    'type' { Type-Text -Text $Text }
    'key' { Press-Key -KeyName $Key }
    'hotkey' {
        $keys = @($Arg1, $Arg2)
        if ($Arg3) { $keys += $Arg3 }
        Press-Hotkey -Keys $keys
    }
    'screenshot' { Take-Screenshot -FilePath $Path }
    'screensize' { Get-ScreenSize }
    default { Show-Help }
}
