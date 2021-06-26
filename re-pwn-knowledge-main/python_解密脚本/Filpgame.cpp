// 1代表反面 0代表正面 最终结果全部翻0

#include<stdio.h>
#include<iostream>
#include<string.h>
#include<math.h>
#include<algorithm>
#include<queue>
#include<stack>
#include<set>
#include<vector>
#include<map>
#define ll long long
#define pi acos(-1)
#define inf 99999999
using namespace std;
typedef pair<int,int>P;
int m,n;
int mp[20][20],flip[20][20],ans[20][20];//原数组、临时数组、结果数组
int go[5][2]={0,0,1,0,0,1,-1,0,0,-1};
int getcolor(int i,int j){//判断某块地是正面还是反面
    int sum=mp[i][j];
    for(int k=0;k<5;k++){
        int di=i+go[k][0];
        int dj=j+go[k][1];
        if(0<=di&&di<m&&0<=dj&&dj<n)
        sum+=flip[di][dj];
    }
    return sum&1;
}
int check(){//确定第一行的状态下判断是否有可行解
    for(int j=1;j<m;j++){
        for(int k=0;k<n;k++){
            flip[j][k]=getcolor(j-1,k);
        }
    }
    for(int i=0;i<n;i++)
    if(getcolor(m-1,i))
    return -1;
    int sum=0;
    for(int i=0;i<m;i++)
    for(int j=0;j<n;j++)
    sum+=flip[i][j];
    return sum;
}
void solve(){
    int res=inf;
    for(int i=0;i<1<<n;i++){//枚举第一行状态
        memset(flip,0,sizeof(flip));
        for(int j=0;j<n;j++){
            flip[0][n-1-j]=(i>>j)&1;//集合的整数表示
        }
        int t=check();
         if(t>=0&&res>t){
            res=t;
            memcpy(ans,flip,sizeof(flip));
         }
    }
    if(res==inf)
    printf("IMPOSSIBLE\n");
    else{
        for(int i=0;i<m;i++){
            printf("[");
            for(int j=0;j<n;j++)
                printf("%d%c",ans[i][j],",]"[j==n-1]);
            printf(",");
        }
    }
}
int main(){
    while(~scanf("%d%d",&m,&n)){
        for(int i=0;i<m;i++)
        	for(int j=0;j<n;j++)
        		scanf("%d",&mp[i][j]);
        solve();
    }
    return 0;
}

//得到的是需要翻转的地方 需要翻转的标为1 不需要翻转的标为0