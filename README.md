# WBENC

This is a Python3 wubi encoder and decoder. The given dict.pkl file is for wubi86.

## Usage

In any terminal:
```bash
$ python wbenc.py -i input.txt -o output.txt -d dict.pkl -E
```

For more usage:
```bash
$ python wbenc.py -h
```

## Example

```bash
$ cat test.txt
人有两个宝，双手和大脑。
爨邯汕寺武穆云籍鞲
　　可是，即使是这样，驘赢臝「；饌餩」的出现仍然代表了一定的意义。 我认为， 驘赢臝「；饌餩」的发生，到底需要如 何做到，不驘赢臝「；饌餩」的发生，又会如何产生。 本人也是经过了深思熟虑，在每个日日夜夜思考这个问题。 富兰克林 说过一句富有哲理的话，读书是易事，思索是难事，但两者缺一，便全无用处。我希望诸位也能好好地体会这句话。 我们一般认为，抓住了问题的关键，其他一切则会迎刃而解。 所谓驘赢臝「；饌餩」，关键是驘赢臝「；饌餩」需要如何写。
$ python wbenc.py -E -i test.txt -o output.txt
$ cat output.txt
w e gmwwwh pgy，cc rt t dd eyb。
wfmoafb imh ff gah tri fcu'tdijafff'
　　sk j，vcb wgkqj p su，ynky8ynkyynky6「；wpnwwpww」r bm gm we qd wa ge b g pg r ujn yq。 q yw o， ynky8ynkyynky6「；wpnwwpww」r v tg，gc yqa fdm s vk wsk wdt gc，i ynky8ynkyynky6「；wpnwwpww」r v tg，ccc wf vk wsk u tg 。 sg w bn j x fp b ipw ln ybv han，d txg wh jjjjjjjjywt ywt ln ftg p wh ukd jghm。 pgk uff dq ss yu fp g qkd pgk e rrk gj r ytd，yfn nnh j jqr gk，ln fpx j cw gk，wjg gmwwftj rmn g，wgj wg fq et th。q qdm ynegyft wug bn ce vb vb f wsg wf p qkd ytd。 q wu g tem yw o，rrhywyggb ukd jghmr ud qvfp，adw wb g av mj wf qbp vyi;dmj qev。 rn yle ynky8ynkyynky6「；wpnwwpww」，ud qvfpj ynky8ynkyynky6「；wpnwwpww」fdm s vk wsk pgn。
$ python wbenc.py -D -i output.txt -o output2.txt
$ diff test.txt output2.txt
$
```


