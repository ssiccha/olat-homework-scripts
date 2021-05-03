Scripts to manage student homework and feedback downloaded from and uploaded to
an OpenOlat instance.

## Rough description (in german)

Man braucht hauptsächlich die Skripte `unpack-clean-compress-submissions.sh` und `prepare-bulk-assessment.py`.
Mein Workflow pro Blatt war dann ungefähr so:

### Blatt erstellen
- Im Olat hab ich für eine Aufgabe "Blatt X" erstellt. Unter dem Reiter Workflow habe ich dann eingestellt, dass die Studis aufgaben ins Olat hochladen können.

### Abgaben runterladen
- Nachdem die Studis das bearbeitet haben, habe ich die Abgaben per "Alle abgegebenen Dokumente herunterladen" als Zip-Datei "Blatt_X..." runtergeladen.
- Die Zip-Datei "Blatt_X..." habe ich per `~/Seafile/exercise-scripts/unpack-clean-compress-submissions.sh X` entpackt, aufgeräumt und komprimiert und in einen Ordner `blatt-X` geschoben.
- (optional) Mit `~/Seafile/exercise-scripts/sort-submissions-into-groups.py X` habe ich für jeden HiWi einen Ordner `gruppe-?` mit seinen/ihren Abgaben gemacht.
- Die Abgaben habe ich dann in einen Seafile-Ordner getan auf den die HiWis Lese-Zugriff hatten. Die haben die Korrekturen dann in einen anderen Seafile Ordner getan, sagen wir `korrekturen-X`. Wichtig war, dass die Ordnerstruktur nicht verändert wurde.

### Abgaben hochladen
- Falls ich den optionalen Schritt gemacht habe, musste ich alle Studenten-Ordner in den Hauptordner verschieben und zwar per `mv korrekturen-X/gruppe-*/* korrekturen-X`
- Zu guter Letzt hab ich per
  ```
    ~/Seafile/exercise-scripts/prepare-bulk-assessment.py korrekturen-X
  ```
  eine zip-datei `upload-to-olat.zip` erstellt. Die konnte ich dann per Massenbewertung direkt ins Olat hochladen.

Diese Massenbewertung erreicht man im Olat per:

    Administration > Bewertungswerkzeug

Dann

    "Liste aller bewertbaren Elemente" > Kursbausteine > Blatt X > "Neue Massenbewertung starten"
