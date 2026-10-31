#!/bin/zsh
# Routing eval: which skill does a fresh Claude Code session load first? Runs every case RUNS times.
# Guards: </dev/null, kill timer, login precheck, exit capture. Usage: run_routing.sh [out_dir] [runs]
EVAL=${0:A:h}
OUT=${1:-$TMPDIR/film-crew-routing}; RUNS=${2:-2}
mkdir -p $OUT; LOG=$OUT/results.tsv; : > $LOG
claude -p "ok" --max-turns 1 < /dev/null > /dev/null 2>&1 || { echo "login/limit precheck failed"; exit 0; }
python3 -I -c "import json,sys; [print(c['id']+'\t'+c['expect']+'\t'+c['prompt']) for c in json.load(open(sys.argv[1]))['cases']]" $EVAL/routing.json > $OUT/cases.tsv
while IFS=$'\t' read -r id expect prompt; do
  for r in $(seq 1 $RUNS); do
    d=$OUT/$id-$r; mkdir -p $d; cd $d
    claude -p "$prompt" --output-format stream-json --verbose --max-turns 2 --allowedTools "Skill" < /dev/null > stream.jsonl 2>/dev/null &
    CPID=$!; ( sleep 180; kill -TERM $CPID 2>/dev/null ) & TPID=$!; wait $CPID; rc=$?; kill $TPID 2>/dev/null
    got=$(python3 -I -c "
import json,sys
for l in open(sys.argv[1],encoding='utf-8'):
    try: e=json.loads(l)
    except: continue
    if e.get('type')=='assistant':
        for c in e['message'].get('content',[]):
            if c.get('type')=='tool_use' and c['name']=='Skill':
                print((c['input'].get('skill') or c['input'].get('command') or '?').split(':')[-1]); sys.exit()
print('none')" stream.jsonl)
    ok=$([[ $got == $expect ]] && echo PASS || echo FAIL)
    printf "%s\t%s\trun%s\texpect=%s\tgot=%s\texit=%s\n" $ok $id $r $expect $got $rc | tee -a $LOG
  done
done < $OUT/cases.tsv
echo "pass: $(grep -c '^PASS' $LOG) / $(wc -l < $LOG)"
