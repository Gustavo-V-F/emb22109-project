# Projeto final de Sistemas Embarcados do IFSC - emb22109

O projeto consiste na manipulação da câmera V2.1 utilizando OpenCV em conjunto da Raspberry Pi Zero W e de motores controlados por PWM. O aplicativo foi desenvolvido em Python e está disponível na pasta `board/emb22109-project/raspberry-pi0w/rootfs-overlay/root/apps/trabalho-final.py`.

A imagem do projeto foi gerada por meio do buildroot, selecionado pela _tag_ 2021.02 no seu repositório. Dessa maneira os seguinte passos foram realizados:

```
git clone git://git.buildroot.net/buildroot
git checkout 2021.02
cd buildroot
cp -rf ../emb22109_project_defconfig ../emb22109_project_linux_defconfig ../board/ ../output/ ../package/ buildroot/ 
make emb22109_project_defconfig
```

Após estes passos, foi adicionado manualmente a linha `source "package/python-picamera/Config.in"` ao arquivo `package/Config.in` na seção de pacotes Python, e então foi feita a compilação com o comando `make`. Esse processo gera na pasta `output/images` os arquivos `bcm2708-rpi-zero-w.dtb`, `zImage`, `rootfs.tar` e a pasta `rpi-firmware`.

Devem ser gravados na partição de _boot_ do seu cartão microSD os arquivos `bcm2708-rpi-zero-w.dtb`, `zImage` e todos dentro da pasta `rpi-firmware` (não copiar a pasta `rpi-firmware`, somente seus arquivos) e para a partição do sistema de arquivos deve ser gravado o arquivo extraído de `rootfs.tar`.

Ao final, pode-se acessar o dispositivo pela sua rede `EMB22109-project` de senha `emb22109-rpi0w`, e seu acesso ssh é feito por `ssh root@rpi0w.local` ou `ssh root@192.168.7.1` com sua senha _root_ `emb22109`.

**Atenção:** o processo de _boot_ é lento, levando cerca de 2 minutos para a inicialização completa.


