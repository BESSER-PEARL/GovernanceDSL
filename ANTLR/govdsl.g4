grammar govdsl;

// Parser rules
project             : 'Project' ID '{'   (roles | deadlines | rules)*  '}' EOF;
// attribute           : roles | deadlines | rules ;
roles               : 'Roles' ':' role (',' role)*  ;
role                : ID ; // check if needed - Because we access from other points
deadlines           : 'Deadlines' ':'  deadline+  ;
deadline            : deadlineID ':' INT timeUnit ;
deadlineID          : ID ;
rules               : 'Rules' ':'  rule+ ;
rule                : ruleID ':' ruleType '{'  ruleContent  '}'  ; // ruleContent depending on ruleType
ruleID              : ID ;
ruleContent         : appliedTo 
                    | people 
                    | minVotes // Can we restrict this attribute to a particular ruleType in ANTLR?
                    | 'deadline' ID 
                    | 'default' ID ;
                    // | 'phases' '{'  phase+ '}' ;
// phase               : ATTR_ID  ;
appliedTo           : 'applied to' taskID ;
taskID              : 'Issue' | 'Pull request' ;
people              : 'people' role (',' role)* ;
minVotes            : 'minVotes' INT ; 
timeUnit            : 'days' | 'weeks' | 'months' | 'years' ;
ruleType            : 'Majority' | 'LeaderDriven' | 'Ratio' ; // | 'Phased' |  ;

// Lexer rules
ID              : [a-zA-Z_][a-zA-Z0-9_]* ;
ATTR_ID         : [a-z][a-zA-Z0-9_]* ; // TODO: ATTR_ID error comes from declaration, overlays on ID, check declaration order
INT             : [0-9]+ ;
// NL              : ('\r'? '\n')+ ;
WS              : (' ' | '\t' | '\r'? '\n')+ -> skip ;