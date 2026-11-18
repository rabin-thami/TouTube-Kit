param([string]$TextFile, [string]$OutWav, [string]$Voice = "Microsoft David Desktop")
# Speaks a UTF-8 text file to a 24 kHz mono 16-bit WAV; prints one JSON line per word: {"w":..., "ms":...}
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SelectVoice($Voice)
$fmt = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(24000, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
$s.SetOutputToWaveFile($OutWav, $fmt)
$words = New-Object System.Collections.ArrayList
Register-ObjectEvent -InputObject $s -EventName SpeakProgress -Action {
  [void]$Event.MessageData.Add(@{ w = $EventArgs.Text; ms = [int]$EventArgs.AudioPosition.TotalMilliseconds })
} -MessageData $words -SourceIdentifier tts | Out-Null
$s.Speak([IO.File]::ReadAllText($TextFile, [Text.Encoding]::UTF8))
# events are delivered asynchronously: wait until the count stops growing
do { $n = $words.Count; Start-Sleep -Milliseconds 300 } while ($words.Count -ne $n)
Unregister-Event tts
$s.Dispose()
foreach ($x in $words.ToArray()) { [pscustomobject]$x | ConvertTo-Json -Compress }
