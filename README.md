## Version Control
* OS: Ubuntu18.04
* gcc: 7.3.0
* boost: 1.65.1

## GCC
* [gcc 버전 컨트롤](https://promobile.tistory.com/377)
* gcc, g++ 모두 7버전 사용

## BOOST
* [공식문서](https://www.boost.org/users/history/version_1_65_1.html)
```bash
$ tar -svf boost_1_65_1.tar.gz
```

## ENV
* Utagger가 이해할 수 있는 경로 설정
```bash
# .bashrc
echo export LD_LIBRARY_PATH=/home/ubuntu/boost_1_65_1/stage/lib > ./.bashrc
echo export UTAGGER_PATH=/home/ubuntu/utagger/bin/ > ./.bashrc
echo export HLX_PATH=/home/ubuntu/utagger/ > ./.bashrc
source ./.bashrc
```
