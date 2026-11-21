$ErrorActionPreference = 'Stop'
$ffmpeg = Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.1-full_build\bin\ffmpeg.exe'
$root = (Get-Location).Path
$assets = Join-Path $root 'video\assets'
$out = Join-Path $root 'video\taiwan-travel-promo-30s.mp4'
$filter = @"
[0:v]zoompan=z='min(1+0.028*on/239,1.028)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1280x720:fps=24,trim=duration=10,setpts=PTS-STARTPTS,format=yuv420p[v0];
[1:v]zoompan=z='min(1+0.028*on/239,1.028)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1280x720:fps=24,trim=duration=10,setpts=PTS-STARTPTS,format=yuv420p[v1];
[2:v]zoompan=z='min(1+0.028*on/239,1.028)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1280x720:fps=24,trim=duration=10,setpts=PTS-STARTPTS,format=yuv420p[v2];
[v0][v1][v2]concat=n=3:v=1:a=0,format=yuv420p[vout];
[3:a]adelay=0|0,volume=1.0[vx0];
[4:a]adelay=10000|10000,volume=1.0[vx1];
[5:a]adelay=20000|20000,volume=1.0[vx2];
[6:a]volume=0.24,afade=t=in:d=1,afade=t=out:st=28:d=2[music];
[vx0][vx1][vx2][music]amix=inputs=4:duration=longest:normalize=0,alimiter=limit=0.95,atrim=duration=30[aout]
"@ -replace '\r?\n',''
$argsList = @(
  '-y',
  '-loop','1','-framerate','24','-t','10','-i',(Join-Path $assets 'scene-01.png'),
  '-loop','1','-framerate','24','-t','10','-i',(Join-Path $assets 'scene-02.png'),
  '-loop','1','-framerate','24','-t','10','-i',(Join-Path $assets 'scene-03.png'),
  '-i',(Join-Path $assets 'voice-01.wav'),
  '-i',(Join-Path $assets 'voice-02.wav'),
  '-i',(Join-Path $assets 'voice-03.wav'),
  '-i',(Join-Path $assets 'music.wav'),
  '-filter_complex',$filter,'-map','[vout]','-map','[aout]','-t','30','-r','24',
  '-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p',
  '-c:a','aac','-b:a','192k','-movflags','+faststart',$out
)
& $ffmpeg @argsList
if ($LASTEXITCODE -ne 0) { throw "FFmpeg encoding failed with exit code $LASTEXITCODE" }
Get-Item -LiteralPath $out | Select-Object FullName,Length

