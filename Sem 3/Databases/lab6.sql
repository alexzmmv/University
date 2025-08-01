ALTER VIEW ViewTaTb AS
SELECT 
    T.aid, 
    T.a2, 
    B.bid, 
    B.b2, 
    C.cid
FROM 
    Ta T
JOIN 
    Tb B 
ON 
    T.aid = B.bid
JOIN 
    Tc C
ON 
    T.aid = C.aid AND B.bid = C.bid
WHERE 
    T.a2 > 10;

GO
/*
<ShowPlanXML xmlns="http://schemas.microsoft.com/sqlserver/2004/07/showplan" Version="1.539">
    <BatchSequence>
        <Batch>
            <Statements>
                <StmtSimple StatementText="SELECT * FROM ViewTaTb" StatementId="1"
                    StatementCompId="1" StatementType="SELECT" RetrievedFromCache="true"
                    StatementSubTreeCost="0.0868778" StatementEstRows="222.298">
                </StmtSimple>
            </Statements>
        </Batch>
    </BatchSequence>
</ShowPlanXML>
*/
SET STATISTICS IO ON;
SET STATISTICS TIME ON;
SET STATISTICS XML ON;
SELECT * FROM ViewTaTb;  
SET STATISTICS XML OFF;
SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;


create NONCLUSTERED INDEX idx_Tb_bid ON Tb;
CREATE nonCLUSTERED INDEX idx_Tc_aid_bid ON Tc(bid,aid);
CREATE nonCLUSTERED INDEX idx_Tc_bid ON Tc(bid);
CREATE nonCLUSTERED INDEX idx_Tc_aid ON Tc(aid);


/*
<ShowPlanXML xmlns="http://schemas.microsoft.com/sqlserver/2004/07/showplan" Version="1.539">
    <BatchSequence>
        <Batch>
            <Statements>
                <StmtSimple StatementText="SELECT * FROM ViewTaTb" StatementId="1"
                    StatementCompId="1" StatementType="SELECT" RetrievedFromCache="true"
                    StatementSubTreeCost="0.0831741" StatementEstRows="222.298">
                </StmtSimple>
            </Statements>
        </Batch>
    </BatchSequence>
</ShowPlanXML>
*/
SET STATISTICS IO ON;
SET STATISTICS TIME ON;
SET STATISTICS XML ON;
SELECT * FROM ViewTaTb; 
SET STATISTICS XML OFF;
SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;



ecaterina.catargiu@gmail.com
