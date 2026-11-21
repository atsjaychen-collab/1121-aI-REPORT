$ErrorActionPreference = 'Stop'

$assets = Join-Path $PSScriptRoot 'assets'
$out = Join-Path $PSScriptRoot 'taiwan-travel-promo-30s.mp4'
$pptxPath = Join-Path $PSScriptRoot 'taiwan-travel-promo-source.pptx'

$app = $null
$presentation = $null
try {
    $app = New-Object -ComObject PowerPoint.Application
    $app.Visible = -1
    $presentation = $app.Presentations.Add(-1)
    $presentation.PageSetup.SlideSize = 16 # ppSlideSizeOnScreen16x9

    $sceneNames = @('scene-01.png', 'scene-02.png', 'scene-03.png')
    $voiceNames = @('voice-01.wav', 'voice-02.wav', 'voice-03.wav')
    for ($i = 0; $i -lt 3; $i++) {
        $slide = $presentation.Slides.Add($i + 1, 12) # ppLayoutBlank
        $scenePath = Join-Path $assets $sceneNames[$i]
        [void]$slide.Shapes.AddPicture($scenePath, 0, -1, 0, 0, 960, 540)

        $slide.SlideShowTransition.AdvanceOnTime = -1
        $slide.SlideShowTransition.AdvanceTime = 10
        $slide.SlideShowTransition.AdvanceOnClick = 0

        $voicePath = Join-Path $assets $voiceNames[$i]
        $voice = $slide.Shapes.AddMediaObject2($voicePath, 0, -1, -100, -100, 1, 1)
        $voice.AnimationSettings.PlaySettings.PlayOnEntry = -1
        $voice.AnimationSettings.PlaySettings.HideWhileNotPlaying = -1
        $voice.AnimationSettings.PlaySettings.StopAfterSlides = 1
    }

    $musicPath = Join-Path $assets 'music.wav'
    $music = $presentation.Slides.Item(1).Shapes.AddMediaObject2($musicPath, 0, -1, -100, -100, 1, 1)
    $music.AnimationSettings.PlaySettings.PlayOnEntry = -1
    $music.AnimationSettings.PlaySettings.HideWhileNotPlaying = -1
    $music.AnimationSettings.PlaySettings.LoopUntilStopped = 0
    $music.AnimationSettings.PlaySettings.StopAfterSlides = 3

    $presentation.SaveAs($pptxPath, 24) # ppSaveAsOpenXMLPresentation
    $presentation.CreateVideo($out, -1, 10, 720, 24, 85)

    $deadline = (Get-Date).AddMinutes(5)
    do {
        Start-Sleep -Seconds 2
        $status = $presentation.CreateVideoStatus
        if ((Get-Date) -gt $deadline) { throw 'PowerPoint video export timed out.' }
        if ($status -eq 4) { throw 'PowerPoint reported a video export failure.' }
    } while ($status -ne 3)

    Get-Item -LiteralPath $out | Select-Object FullName, Length, LastWriteTime
}
finally {
    if ($presentation -ne $null) { $presentation.Close() }
    if ($app -ne $null) { $app.Quit() }
    if ($presentation -ne $null) { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation) }
    if ($app -ne $null) { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app) }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
