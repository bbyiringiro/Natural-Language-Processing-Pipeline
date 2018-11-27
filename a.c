#include <stdio.h>
#include <math.h>
     
                                                                                                           
int main(){
                /*Function Prototypes*/
    int scoreTable[4][4]; // holding teams as rows and points, goals difference, goals, and teams indeces as columns 
    int a, b; // variable holds goals of two teams from matches

    int r, c, x, temp; // row, col , x, temp variables to use in loops
    int goalD=0; // loop gifference
	printf("Enter scores for A:B,A:C,A:D,B:C,B:D and C:D in that order\n");             
    
    do{
		// initializing the table initially for 0
		for (r =0; r<=3; r++){
		scoreTable[r][3]=r; // give every team an index 0 = A, 1= B, 2=C, 3 = D
			for (c=0; c <3; c++){
				scoreTable[r][c]=0;
			}
    	}

		

		/*Reading in Match Results*/
		
		for (r =0; r<3; r++){
			for (c=r+1; c<=3; c++){
				scanf("%d %d", &a,&b);
				goalD=a-b;
				
				scoreTable[r][2] +=a;
				scoreTable[c][2] +=b;
				
				
				if(a>b){
					scoreTable[r][0] +=3;
					scoreTable[c][0] +=0;
					scoreTable[r][1] +=goalD;
					scoreTable[c][1] -=goalD;		
								
				}else if (b>a){
					scoreTable[r][0] +=0;
					scoreTable[c][0] +=3;
					scoreTable[r][1] += goalD;
					scoreTable[c][1] -= goalD;
				}
				else {
					scoreTable[c][0] +=1;
					scoreTable[r][0] +=1;
				}
				
							
			}
		}
	
	// ranking
	for (int i = 0; i < 4; i++)                    
	{
		for (int j = i+1; j < 4; j++)             
		{
			
			//rank by points
			if (scoreTable[j][0] <  scoreTable[i][0]){
				// swap all tables column
				for(x=0;x<4;x++) {
                    temp = scoreTable[i][x];  
					scoreTable[i][x] = scoreTable[j][x];            
					scoreTable[j][x] = temp; 
                }
			            
			}else if (scoreTable[j][0] ==  scoreTable[i][0]){
				// rank by score difference	
				if (scoreTable[j][1] <  scoreTable[i][1])              
				{

					for(x=0;x<4;x++) {
						temp = scoreTable[i][x];  
						scoreTable[i][x] = scoreTable[j][x];            
						scoreTable[j][x] = temp; 
					}
				            
				} else if (scoreTable[j][1] ==  scoreTable[i][1]){
					// rank by goals
					if (scoreTable[j][2] <  scoreTable[i][2])              
					{

						for(x=0;x<4;x++) {
							temp = scoreTable[i][x];  
							scoreTable[i][x] = scoreTable[j][x];            
							scoreTable[j][x] = temp; 
						}
								
					} else if (scoreTable[j][2] ==  scoreTable[i][2]){
						// rank by alphabet ( team indeces)
						if (scoreTable[j][3] <  scoreTable[i][3])              
						{

							for(x=0;x<4;x++) {
								temp = scoreTable[i][x];  
								scoreTable[i][x] = scoreTable[j][x];            
								scoreTable[j][x] = temp; 
							}
									
					}
				}
			}
		}
	}
	}



	printf("Ranking of the teams is ");
	for (r =0; r<=3; r++){
		printf("");
		if (scoreTable[r][3] == 0){
						printf("A");
		}else if (scoreTable[r][3] == 1){
						printf("B");
		}else if (scoreTable[r][3] == 2){
						printf("C");
		}else if (scoreTable[r][3] == 3){
						printf("D");
		}
	
}
	printf(".\n");


}while(EOF);

    return 0;
}