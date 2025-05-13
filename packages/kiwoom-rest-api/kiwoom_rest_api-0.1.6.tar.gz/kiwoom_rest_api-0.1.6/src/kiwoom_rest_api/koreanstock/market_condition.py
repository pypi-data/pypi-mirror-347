from kiwoom_rest_api.core.base_api import KiwoomBaseAPI
from typing import Union, Dict, Any, Awaitable

class MarketCondition(KiwoomBaseAPI):
    """한국 주식 시장 조건 관련 API를 제공하는 클래스"""
    
    def __init__(
        self, 
        base_url: str = None, 
        token_manager=None, 
        use_async: bool = False,
        resource_url: str = "/api/dostk/mrkcond"
    ):
        """
        MarketCondition 클래스 초기화
        
        Args:
            base_url (str, optional): API 기본 URL
            token_manager: 토큰 관리자 객체
            use_async (bool): 비동기 클라이언트 사용 여부 (기본값: False)
        """
        super().__init__(
            base_url=base_url,
            token_manager=token_manager,
            use_async=use_async,
            resource_url=resource_url
        )
        
    def stock_quote_request_ka10004(
        self,
        stock_code: str,
        cont_yn: str = "N",
        next_key: str = ""
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """주식호가요청

        Args:
            stock_code (str): 종목코드 (예: "005930", "KRX:039490")
            cont_yn (str, optional): 연속조회여부. Defaults to "N".
            next_key (str, optional): 연속조회키. Defaults to "".

        Returns:
            Union[Dict[str, Any], Awaitable[Dict[str, Any]]]: 응답 데이터
            {
                "bid_req_base_tm": "162000",
                "sel_10th_pre_req_pre": "0",
                "sel_10th_pre_req": "0",
                "sel_10th_pre_bid": "0",
                ...
                "ovt_buy_req_pre": "0",
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        headers = {
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10004"
        }
        data = {
            "stk_cd": stock_code
        }
        return self._execute_request("POST", json=data, headers=headers)
    
    def stock_daily_weekly_monthly_time_request_ka10005(
        self,
        stock_code: str,
        cont_yn: str = "N",
        next_key: str = ""
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """주식일주월시분요청

        Args:
            stock_code (str): 종목코드 (예: "005930", "KRX:039490")
            cont_yn (str, optional): 연속조회여부. Defaults to "N".
            next_key (str, optional): 연속조회키. Defaults to "".

        Returns:
            Union[Dict[str, Any], Awaitable[Dict[str, Any]]]: 응답 데이터
            {
                "stk_ddwkmm": [
                    {
                        "date": "20241028",
                        "open_pric": "95400",
                        "high_pric": "95400",
                        "low_pric": "95400",
                        "close_pric": "95400",
                        "pre": "0",
                        "flu_rt": "0.00",
                        "trde_qty": "0",
                        "trde_prica": "0",
                        "for_poss": "+26.07",
                        "for_wght": "+26.07",
                        "for_netprps": "0",
                        "orgn_netprps": "",
                        "ind_netprps": "",
                        "crd_remn_rt": "",
                        "frgn": "",
                        "prm": ""
                    },
                    ...
                ]
            }
        """
        headers = {
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10005"
        }
        data = {
            "stk_cd": stock_code
        }
        return self._execute_request("POST", json=data, headers=headers)
    
    def stock_minute_time_request_ka10006(
        self,
        stock_code: str,
        cont_yn: str = "N",
        next_key: str = ""
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """주식시분요청

        Args:
            stock_code (str): 종목코드 (예: "005930", "KRX:039490")
            cont_yn (str, optional): 연속조회여부. Defaults to "N".
            next_key (str, optional): 연속조회키. Defaults to "".

        Returns:
            Union[Dict[str, Any], Awaitable[Dict[str, Any]]]: 응답 데이터
            {
                "date": "20241105",
                "open_pric": "0",
                "high_pric": "0",
                "low_pric": "0",
                "close_pric": "135300",
                "pre": "0",
                "flu_rt": "0.00",
                "trde_qty": "0",
                "trde_prica": "0",
                "cntr_str": "0.00",
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        headers = {
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10006"
        }
        data = {
            "stk_cd": stock_code
        }
        return self._execute_request("POST", json=data, headers=headers)
    
    def market_price_table_info_request_ka10007(
        self,
        stock_code: str,
        cont_yn: str = "N",
        next_key: str = ""
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """시세표성정보요청

        Args:
            stock_code (str): 종목코드 (예: "005930", "KRX:039490")
            cont_yn (str, optional): 연속조회여부. Defaults to "N".
            next_key (str, optional): 연속조회키. Defaults to "".

        Returns:
            Union[Dict[str, Any], Awaitable[Dict[str, Any]]]: 응답 데이터
            {
                "stk_nm": "삼성전자",
                "stk_cd": "005930",
                "date": "20241105",
                "tm": "104000",
                "pred_close_pric": "135300",
                "pred_trde_qty": "88862",
                "upl_pric": "+175800",
                "lst_pric": "-94800",
                "pred_trde_prica": "11963",
                "flo_stkcnt": "25527",
                "cur_prc": "135300",
                "smbol": "3",
                "flu_rt": "0.00",
                "pred_rt": "0.00",
                "open_pric": "0",
                "high_pric": "0",
                "low_pric": "0",
                "cntr_qty": "",
                "trde_qty": "0",
                "trde_prica": "0",
                "exp_cntr_pric": "-0",
                "exp_cntr_qty": "0",
                "exp_sel_pri_bid": "0",
                "exp_buy_pri_bid": "0",
                "trde_strt_dt": "00000000",
                "exec_pric": "0",
                "hgst_pric": "",
                "lwst_pric": "",
                "hgst_pric_dt": "",
                "lwst_pric_dt": "",
                "sel_1bid": "0",
                "sel_2bid": "0",
                ...
                "buy_10bid_req": "0",
                "tot_buy_req": "0",
                "tot_sel_req": "0",
                "tot_buy_cnt": "",
                "tot_sel_cnt": "0",
                "return_code": 0,
                "return_msg": "정상적으로 처리되었습니다"
            }
        """
        headers = {
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10007"
        }
        data = {
            "stk_cd": stock_code
        }
        return self._execute_request("POST", json=data, headers=headers)
    
    def rights_issue_overall_price_request_ka10011(
        self,
        rights_type: str,
        cont_yn: str = "N",
        next_key: str = ""
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """신주인수권전체시세요청

        Args:
            rights_type (str): 신주인수권구분 (00:전체, 05:신주인수권증권, 07:신주인수권증서)
            cont_yn (str, optional): 연속조회여부. Defaults to "N".
            next_key (str, optional): 연속조회키. Defaults to "".

        Returns:
            Union[Dict[str, Any], Awaitable[Dict[str, Any]]]: 응답 데이터
            {
                "newstk_recvrht_mrpr": [
                    {
                        "stk_cd": "J0036221D",
                        "stk_nm": "KG모빌리티 122WR",
                        "cur_prc": "988",
                        "pred_pre_sig": "3",
                        "pred_pre": "0",
                        "flu_rt": "0.00",
                        "fpr_sel_bid": "-0",
                        "fpr_buy_bid": "-0",
                        "acc_trde_qty": "0",
                        "open_pric": "-0",
                        "high_pric": "-0",
                        "low_pric": "-0"
                    },
                    ...
                ]
            }
        """
        headers = {
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10011"
        }
        data = {
            "newstk_recvrht_tp": rights_type
        }
        return self._execute_request("POST", json=data, headers=headers)
    
    def daily_institutional_trading_items_request_ka10044(
        self,
        start_date: str,
        end_date: str,
        trade_type: str,
        market_type: str,
        stock_exchange_type: str,
        cont_yn: str = "N",
        next_key: str = ""
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """일별기관매매종목요청

        Args:
            start_date (str): 시작일자 (YYYYMMDD)
            end_date (str): 종료일자 (YYYYMMDD)
            trade_type (str): 매매구분 (1:순매도, 2:순매수)
            market_type (str): 시장구분 (001:코스피, 101:코스닥)
            stock_exchange_type (str): 거래소구분 (1:KRX, 2:NXT, 3:통합)
            cont_yn (str, optional): 연속조회여부. Defaults to "N".
            next_key (str, optional): 연속조회키. Defaults to "".

        Returns:
            Union[Dict[str, Any], Awaitable[Dict[str, Any]]]: 응답 데이터
            {
                "daly_orgn_trde_stk": [
                    {
                        "stk_cd": "005930",
                        "stk_nm": "삼성전자",
                        "netprps_qty": "-0",
                        "netprps_amt": "-1",
                        "prsm_avg_pric": "140000",
                        "cur_prc": "-95100",
                        "avg_pric_pre": "--44900",
                        "pre_rt": "-32.07"
                    },
                    ...
                ]
            }
        """
        headers = {
            "cont-yn": cont_yn,
            "next-key": next_key,
            "api-id": "ka10044"
        }
        data = {
            "strt_dt": start_date,
            "end_dt": end_date,
            "trde_tp": trade_type,
            "mrkt_tp": market_type,
            "stex_tp": stock_exchange_type
        }
        return self._execute_request("POST", json=data, headers=headers)