# Kubeflow を EKS 上に構築する

## なぜEKS ?

社内のセキュリティの理由で、AWSの東京リージョンでなければ構築できないという大人な事情です。また、高額であるためGPUインスタンスを利用することもできないという大人な事情があるために、安価なCPUインスタンスで構築をします。そのために、[公式ドキュメント](https://aws.amazon.com/jp/blogs/opensource/kubeflow-amazon-eks/) からは若干ずれたものであるので、ドキュメントとして残しておこうかと思います。

## 必要な条件

* AWS CLI
* EKS Optimized AMI
  * 日本リージョンのCPUインスタンス: `ami-063650732b3e8b38c`
  * 日本リージョンのGPUインスタンス: `ami-080be783089a635dd`
* `kubectl` 
  * `brew install kubectl`

* `eksctl`
  * `brew install weaveworks/tap/eksctl`
* `ksonnet`
  * `brew install ksonnet/tap/ks`

## やりかた

### クラスタの作成

```shell
$ eksctl create cluster eks-kubeflow --node-type=t2.large --nodes 2 --region ap-northeast-1 --timeout=40m
```

安いクラスタにするために、一旦 `t2.large` で作成。東京リージョンは `ap-northeast-1` 。

公式ドキュメントでは、GPUを動かすために、Kubernetes 用のDevice PluginのDaemonsetを用意していますが、CPUインスタンスで構築したいので、一旦無視

```shell
$ kubectl get daemonset -n kube-system
NAME         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
aws-node     2         2         2       2            2           <none>          15m
kube-proxy   2         2         2       2            2           <none>          15m
```

### Storage Class の作成

公式ドキュメント曰く、Kubeflowで使える Jupyter Hub を利用するのに Persistent Volume が必要になるので、Kubernetesに作る必要がある。

```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: gp2
  annotations:
    storageclass.beta.kubernetes.io/is-default-class: "true"
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
reclaimPolicy: Delete
mountOptions:
  - debug
```

どうやらキモとなる部分はparametes以下のtypeの項目。ここでAWS上で利用できるEBSタイプを選択するらしい。ただし、 `gp2` はデフォルトで設定されているようなので、一旦無視。

### KubeflowのInstall

Kubeflowはksonnetを活用して、yamlを自動的に生成し、CRDに様々な機能を登録している。そのために、ksonnetが使える状態でなければいけないので、設定をしておく。

Kubeflow用のnamespaceを登録。

```
kubectl create namespace kubeflow
```

公式ドキュメントによると、Kubeflow用のdownload scriptを実行するのだが、必ず `KUBEFLOW_VERSION` を指定しなければならない。中身のshellを見ると、一目瞭然で `KUBEFLOW_VERSION` が変数となっているからである。なお、公式ドキュメントではv0.2であったが、kubeflowのv0.3以降ではインストール方法が異なるために、それ以降は [Getting Started with Kubeflow](https://www.kubeflow.org/docs/started/getting-started/) を参考にした方が良い。

```shell
$ curl https://raw.githubusercontent.com/kubeflow/kubeflow/v0.4.0/scripts/download.sh
#!/usr/bin/env bash
#
# Download the registry and scripts.
# This is the first step in setting up Kubeflow.
# Downloads it to the current directory
set -ex

if [ ! -z "${KUBEFLOW_VERSION}" ]; then
  KUBEFLOW_TAG=v${KUBEFLOW_VERSION}
fi

KUBEFLOW_TAG=${KUBEFLOW_TAG:-master}

# Create a local copy of the Kubeflow source repo
TMPDIR=$(mktemp -d /tmp/tmp.kubeflow-repo-XXXX)
curl -L -o ${TMPDIR}/kubeflow.tar.gz https://github.com/kubeflow/kubeflow/archive/${KUBEFLOW_TAG}.tar.gz
tar -xzvf ${TMPDIR}/kubeflow.tar.gz -C ${TMPDIR}
# GitHub seems to strip out the v in the file name.
KUBEFLOW_SOURCE=$(find ${TMPDIR} -maxdepth 1 -type d -name "kubeflow*")

# Copy over the directories we need
cp -r ${KUBEFLOW_SOURCE}/kubeflow ./
cp -r ${KUBEFLOW_SOURCE}/scripts ./
cp -r ${KUBEFLOW_SOURCE}/deployment ./
```

このスクリプトはkubeflowのrootディレクトリで実行するので、よしななディレクトリを作成する。便宜上はGetting Started with Kubeflowと同じ `KUBEFLOW_SRC`と記す

```shell
$ export KUBEFLOW_VERSION='0.4.0'
$ curl https://raw.githubusercontent.com/kubeflow/kubeflow/v0.4.0/scripts/download.sh | bash

$ ls -l
total 24
-rw-r--r--@  1 kosukekikuchi  staff  4378 Jan  8 09:21 README.md
drwxr-xr-x   3 kosukekikuchi  staff    96 Jan  8 09:21 deployment
drwxr-xr-x  36 kosukekikuchi  staff  1152 Jan  8 09:21 kubeflow
drwxr-xr-x  16 kosukekikuchi  staff   512 Jan  8 09:21 scripts
-rw-r--r--   1 kosukekikuchi  staff   252 Jan  8 08:57 storageclass.yaml
```

`deployment`, `kubeflow`, `scripts`のディレクトリが作成されていることを確認する。次にセットアップとインストールのために、下記のコマンドを実行する

```shell
$ export KFAPP=${KUBEFLOW_SRC}/'kfapp'
$ {KUBEFLOW_SRC}/scripts/kfctl.sh init ${KFAPP} --platform none
$ cd ${KFAPP}
$ {KUBEFLOW_SRC}/scripts/kfctl.sh generate k8s
$ {KUBEFLOW_SRC}/scripts/kfctl.sh apply k8s
```

なお、 `kfctl.sh init` の際に `--zone` のオプションを活用すると GPUインスタンスでも稼働するらしいが、今回はCPUインスタンスを作りたいので、無視。なお、実際に作られるインスタンスはこの通り。

```
$ kubectl get pod -n kubeflow
NAME                                                      READY   STATUS             RESTARTS   AGE
ambassador-5cf8cd97d5-48hkf                               1/1     Running            0          4m
ambassador-5cf8cd97d5-tl8mc                               1/1     Running            0          4m
ambassador-5cf8cd97d5-zrmn9                               1/1     Running            0          4m
argo-ui-7c9c69d464-8d88p                                  1/1     Running            0          4m
centraldashboard-6f47d694bd-xmf6v                         1/1     Running            0          4m
jupyter-0                                                 1/1     Running            0          4m
katib-ui-6bdb7d76cc-jwxc7                                 1/1     Running            0          3m
metacontroller-0                                          1/1     Running            0          4m
minio-7bfcc6c7b9-w5bbb                                    1/1     Running            0          4m
ml-pipeline-b59b58dd6-wztkj                               1/1     Running            0          4m
ml-pipeline-persistenceagent-9ff99498c-ct649              1/1     Running            5          4m
ml-pipeline-scheduledworkflow-78794fd86f-znq7c            1/1     Running            0          4m
ml-pipeline-ui-9884fd997-7zqbs                            1/1     Running            0          3m
ml-pipelines-load-samples-s2ptj                           0/1     Completed          0          3m
mysql-6f6b5f7b64-hqp57                                    1/1     Running            0          4m
spartakus-volunteer-65d49f4794-hl4h4                      1/1     Running            0          4m
studyjob-controller-774d45f695-xpsb5                      0/1     CrashLoopBackOff   4          3m
tf-job-dashboard-5f986cf99d-jlgnl                         1/1     Running            0          4m
tf-job-operator-v1beta1-5876c48976-rrbsz                  1/1     Running            0          4m
vizier-core-fc7969897-7czgx                               1/1     Running            2          3m
vizier-core-rest-6fcd4665d9-2hgn6                         1/1     Running            0          3m
vizier-db-777675b958-drscn                                1/1     Running            0          3m
vizier-suggestion-bayesianoptimization-54db8d594f-tlp85   1/1     Running            0          3m
vizier-suggestion-grid-6f5d9d647f-bhq7m                   1/1     Running            0          3m
vizier-suggestion-hyperband-59dd9bb9bc-xt5dw              1/1     Running            0          3m
vizier-suggestion-random-6dd597c997-h4vj6                 1/1     Running            0          3m
workflow-controller-5c95f95f58-xc6bl                      1/1     Running            0          4m
```

