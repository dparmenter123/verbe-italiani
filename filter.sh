#!/ bin/sh
while read p; do
  egrep $p'.*Condizionale Presente'           $2  | gshuf -n1 
  # egrep $p'.*Condizionale Passato'            $2  | gshuf -n1 
  egrep $p'.*Imperfetto'            $2  | gshuf -n1 
  # egrep $p'.*Indicativo Passato remoto'       $2  | gshuf -n1 
  egrep $p'.*Futuro semplice'      $2  | gshuf -n1 
  egrep $p'.*Passato prossimo'     $2  | gshuf -n1 
  # egrep $p'.*Indicativo Trapassato prossimo'  $2  | gshuf -n1 
  # egrep $p'.*Indicativo Futuro anteriore'     $2  | gshuf -n1 
  # egrep $p'.*Congiuntivo Presente'            $2  | gshuf -n1 
  # egrep $p'.*Congiuntivo Passato'             $2  | gshuf -n1 
  # egrep $p'.*Congiuntivo Trapassato'          $2  | gshuf -n1 
  # egrep $p'.*Congiuntivo Imperfetto'          $2  | gshuf -n1 
done < $1
exit 2

