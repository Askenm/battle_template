# RETURN SERIAL ID RETURNING id;
query_catalog = {
    "write": {
        "CREATE_BATTLE": """
                                          INSERT INTO ckb.battles (battle_name, battle_description, tournament_id, github_repo, creator,end_date)
                                          VALUES ('_BATTLE_NAME_', '_BATTLE_DESC_', _TOURNAMENT_ID_, '_BATTLE_REPO_', '_BATTLE_CREATOR_','_END_DATE_')
                                          RETURNING bid;
                                          """,
        "END_TOURNAMENT": """
                                            UPDATE ckb.tournaments
                                            SET end_date = NOW()
                                            WHERE tid = _TOURNAMENT_ID_;

                                            """,
        "CREATE_TOURNAMENT": """
                                                 INSERT INTO ckb.tournaments (tournament_name, creator)
                                                 VALUES ('_TOURNAMENT_NAME_', '_CREATOR_')
                                                 RETURNING tid;
                                                 """,
        "CREATE_BADGE": """
                            INSERT INTO ckb.badge (badge_name, badge_description, tournament_id, rank, num_battles)
                            VALUES 
                            ('_BADGE_NAME_', '_BADGE_DESC_', _TOURNAMENT_ID_, _RANK_, _NUM_BATTLES_)
                            """,
        "AWARD_BADGE": """
                            INSERT INTO ckb.badgeholders (bid, uid)
                            VALUES 
                            (_BADGE_ID_, _USER_ID_)
                            """,
        "REGISTER_NOTIFICATION": """
                                   INSERT INTO ckb.message_board (uid, notification_type, tournament_id, notification_text, battle_id)
                                   VALUES
                                   (_USER_ID_, '_NOTIFICATION_TYPE_', _TOURNAMENT_ID_, '_NOTIFICATION_TEXT_', _BATTLE_ID_)
                                   """,
       "MARK_NOTIFICATION_AS_SENT":       """
                                          UPDATE ckb.message_board
                                          SET is_sent = TRUE, 
                                          sent_date = CURRENT_DATE
                                          WHERE nid = _NOTIFICATION_ID_;

                                          """,
       "JOIN_GROUP": """
                     INSERT INTO ckb.groups (group_name, bid, uid)
                     VALUES ('_GROUP_NAME_', _BATTLE_ID_, _USER_ID_);

                     """,
       "SUBSCRIBE_TO_TOURNAMENT":  """
                                   INSERT INTO ckb.subscriptions (uid, tid)  
                                   VALUES ( _USER_ID_,_TOURNAMENT_ID_);
                                   """,
       "ASSIGN_MANUAL_SCORE":      """
                                   INSERT INTO ckb.submissions (battle_id, gid,submission_score)
                                   VALUES ( _BATTLE_ID_,_GROUP_ID_,_SCORE_);
                                   """,
       "ASSIGN_AUTOMATIC_SCORE":      """
                            INSERT INTO ckb.submissions (battle_id, gid,submission_score)
                            VALUES ( _BATTLE_ID_,_GROUP_ID_,_SCORE_);
                            """
    },
    "read": {
        "GET_BATTLE_RANKINGS": """SELECT 
                                                 g.group_name,
                                                 MAX(submission_score) as score, 
                                                 COUNT(DISTINCT smid) as num_submissions 
                                                 FROM ckb.battles b
                                                 INNER JOIN ckb.groups g
                                                 ON b.bid = g.bid
                                                 INNER JOIN ckb.submissions s
                                                 ON s.gid = g.gid

                                                 WHERE b.bid = _BATTLE_ID_

                                                 GROUP BY g.group_name
                                                 ORDER BY score desc
                                                 """,
        "GET_BATTLE_PAGE_INFO": """
                                                 SELECT * FROM ckb.battles b
                                                 WHERE b.bid = _BATTLE_ID_
                                                 """,
        "BATTLE_NAME_VACANT": """
                                                 SELECT count(*) AS count FROM ckb.battles 
                                                 WHERE battle_name = '_BATTLE_NAME_'
                                                 """,
        "TOURNAMENT_NAME_VACANT": """
                                                 SELECT count(*) AS count FROM ckb.tournaments 
                                                 WHERE tournament_name = '_TOURNAMENT_NAME_'
                                                 """,
        "GET_TOURNAMENT_RANKINGS": """SELECT 
                                                 u.user_name,
                                                 BattleQuery.score,
                                                 COUNT(distinct BattleQuery.bid) as num_battles

                                                 FROM ckb.tournaments t
                                                 INNER JOIN 
                                                 (SELECT b.bid,
                                                               g.uid,
                                                 MAX(submission_score) as score
                                                 FROM ckb.battles b
                                                 INNER JOIN ckb.groups g
                                                 ON b.bid = g.bid
                                                 INNER JOIN ckb.submissions s
                                                 ON s.gid = g.gid

                                                 GROUP BY b.bid,g.uid
                                                 ) as BattleQuery

                                                 ON t.tid = BattleQuery.bid
                                                 INNER JOIN ckb.users u
                                                 on u.uid = BattleQuery.uid

                                                 WHERE t.tid = _TOURNAMENT_ID_ 

                                                 GROUP BY u.user_name,BattleQuery.score
                                                 ORDER BY BattleQuery.score desc
                                                 """,
        "GET_TOURNAMENT_PAGE_INFO": """
                                                 SELECT tournament_name,creator FROM ckb.tournaments t
                                                 WHERE t.tid = _TOURNAMENT_ID_
                                                 """,
        "GET_RELATED_BATTLES": """
                                                 SELECT b.battle_name,
                                                 CASE WHEN b.end_date < NOW()::DATE
                                                 THEN 'Ended'
                                                 ELSE 'Ongoing'
                                                 END
                                                 as battle_status,
                                                 b.create_date,
                                                 b.end_date
                                                 FROM ckb.battles b
                                                 INNER JOIN 
                                                 ckb.tournaments t
                                                 ON b.tournament_id = t.tid
                                                 
                                                 
                                                 WHERE t.tid = _TOURNAMENT_ID_
                                                 
                                                 ORDER BY b.end_date desc
                                                 
                                                 """,
        "IS_EDUCATOR": """
                            SELECT is_educator FROM ckb.users WHERE uid = _USER_ID_
                            """,
        "GET_USER_GROUP": """
                            SELECT DISTINCT u.uid,g.gid,group_name 
                            FROM ckb.users u
                            INNER JOIN ckb.groups g
                            ON g.uid = u.uid
                            INNER JOIN ckb.battles b
                            ON g.bid = b.bid
                            WHERE u.uid = _USER_ID_
                            AND
                            b.bid = _BATTLE_ID_
                            """,
        "GET_SUBMISSIONS": """
                            SELECT DISTINCT
                            smid,
                            s.gid,
                            group_name,
                            submission_datetime,
                            submission_score
                            FROM
                            ckb.submissions s
                            INNER JOIN ckb.groups g
                            ON s.gid = g.gid

                            WHERE _CONDITIONAL_
                            """,
        "GET_TOURNAMENT_BADGES": """
                                   SELECT badge_name,badge_description
                                   FROM ckb.badge b
                                   WHERE tournament_id = _TOURNAMENT_ID_
                                   """,
        "GET_BADGE_ACHIEVERS": """
                                   WITH RankedSubmissions AS (
                                   SELECT 
                                          s.submission_score, 
                                          g.uid, 
                                          s.battle_id,
                                          b.tournament_id,
                                          RANK() OVER (PARTITION BY s.battle_id ORDER BY s.submission_score DESC) as rank
                                   FROM ckb.submissions s
                                   JOIN ckb.groups g ON s.gid = g.gid
                                   JOIN ckb.battles b ON s.battle_id = b.bid
                                   WHERE b.tournament_id = _TOURNAMENT_ID_
                                   ),
                                   TopUsers AS (
                                   SELECT 
                                          uid, 
                                          COUNT(*) AS top_finishes
                                   FROM RankedSubmissions
                                   WHERE rank <= _RANK_
                                   GROUP BY uid
                                   )
                                   SELECT 
                                   u.uid, 
                                   u.user_name, 
                                   top_finishes
                                   FROM TopUsers tu
                                   JOIN ckb.users u ON tu.uid = u.uid
                                   WHERE top_finishes > _NUM_BATTLES_;
                                   """,
        "GET_BADGE_LOGIC": """
                                   SELECT tournament_id, rank, num_battles 
                                   FROM ckb.badge
                                   WHERE bid = _BADGE_ID_
                                   """,
        "GET_USER_TOURNAMENTS": """
                                   SELECT tournament_name from 
                                   ckb.tournaments t
                                   INNER JOIN ckb.subscriptions s
                                   ON t.tid = s.tid
                                   WHERE s.uid = _USER_ID_
                                   """,
        "GET_USER_BATTLES": """
                                   select battle_name,group_name,b.end_date 
                                   FROM ckb.groups g
                                   INNER JOIN ckb.battles b 
                                   ON b.bid = g.bid 
                                   WHERE g.uid = _USER_ID_
                                   """,
        "GET_USER_BADGES": """
                                   select badge_name,tournament_name,badge_achieved 
                                   FROM ckb.badge b
                                   INNER JOIN ckb.badgeholders bh 
                                   ON b.bid = bh.bid 
                                   INNER JOIN ckb.tournaments t
                                   ON t.tid = b.tournament_id
                                   WHERE bh.uid = _USER_ID_
                                   """,
       "GET_BADGE_NAME":    """
                            SELECT badge_name FROM ckb.badge WHERE bid = _BADGE_ID_
                            """,
       "GET_TOURNAMENT_NAME_FROM_BADGE_ID":      """
                                                 SELECT tournament_id,tournament_name FROM ckb.badge b
                                                 INNER JOIN ckb.tournaments t
                                                 ON b.tournament_id = t.tid
                                                 WHERE bid = _BADGE_ID_ 
                                                 """,
       "GET_USER_NAME_FROM_UID":                 """
                                                 SELECT user_name FROM ckb.users u
                                                 WHERE uid = _USER_ID_
                                                 """,
       "CHECK_MESSAGEBOARD":       """
                                   SELECT u.user_email , m.*FROM ckb.message_board m
                                   inner join ckb.users u
                                   ON u.uid = m.uid
                                   WHERE is_sent = false
                                   """,
       "GET_ALL_BADGES":    """
                            SELECT * FROM ckb.badge b
                            INNER JOIN ckb.tournaments t
                            ON b.tournament_id = t.tid
                            WHERE t.end_date is NULL
                            """,
       "GET_BATTLE_TOURNAMENT":    """
                                   SELECT tournament_id 
                                   """,
       "GET_CURRENT_BADGE_HOLDERS":       """
                                          SELECT * FROM ckb.badgeholders
                                          WHERE bid = _BADGE_ID_
                                          """,
       "GET_TOURNAMENT_NAME":      """
                                   SELECT tournament_name FROM ckb.tournaments t
                                   WHERE tid = _TOURNAMENT_ID_
                                   """,

       "GET_UNASSIGNED_SUBSCRIBERS":    """
              SELECT u.uid,u.user_name FROM 
              ckb.battles b 
              INNER JOIN ckb.tournaments t
              ON b.tournament_id = t.tid
              INNER JOIN ckb.subscriptions s
              ON s.tid = t.tid
              INNER JOIN ckb.users u
              ON s.uid = u.uid

              WHERE 
              b.bid = _BATTLE_ID_
              AND
              u.uid NOT IN 
              (SELECT g.uid FROM 
              ckb.battles b 
              INNER JOIN ckb.tournaments t
              ON b.tournament_id = t.tid
              INNER JOIN ckb.groups g
              ON g.bid = b.bid
              WHERE b.bid = _BATTLE_ID_)
              """,
       "GET_GROUP_ID_FROM_GROUP_NAME":    """
                                          select g.* from ckb.groups g
                                          inner join ckb.battles b
                                          on g.bid = b.bid
                                          WHERE 
                                          group_name = '_GROUP_NAME_'
                                          AND
                                          battle_name = '_BATTLE_NAME_'
                                          """
    },
}
