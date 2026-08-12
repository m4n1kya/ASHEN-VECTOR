import numpy as np
import pandas as pd
from typing import List, Dict, Optional
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression
import lightgbm as lgb
import logging

logger = logging.getLogger(__name__)

class LiveModelEngine:
    def __init__(self):
        pass

    def run_momentum(self, df: pd.DataFrame, horizon: int) -> dict:
        try:
            if len(df) < 252:
                return None
            
            current_price = df['Close'].iloc[-1]
            
            # Calculate multi-timeframe momentums
            def get_mom(days):
                return (current_price / df['Close'].iloc[-days-1]) - 1.0
                
            mom_5 = get_mom(5)
            mom_21 = get_mom(21)
            mom_63 = get_mom(63)
            mom_126 = get_mom(126)
            mom_252 = get_mom(252)
            
            # Historical means/stds for normalization (proxy using current price series)
            # In a real system, you'd track the rolling mean/std of these momentums.
            # Here we just use the raw percentage.
            
            composite = np.mean([mom_5, mom_21, mom_63, mom_126, mom_252])
            
            expected_ret = composite * (horizon / 252) # Scale to horizon
            prob_up = 1.0 / (1.0 + np.exp(-composite * 10))
            
            return {
                "expected_return": expected_ret, 
                "probability_up": prob_up, 
                "name": "Momentum",
                "details": {
                    "5D": float(mom_5),
                    "21D": float(mom_21),
                    "63D": float(mom_63),
                    "126D": float(mom_126),
                    "252D": float(mom_252),
                    "Composite": float(composite)
                }
            }
        except Exception as e:
            logger.error(f"Momentum failed: {e}")
            return None

    def run_mean_reversion(self, df: pd.DataFrame, horizon: int) -> dict:
        # Ornstein-Uhlenbeck Process
        try:
            if len(df) < 252:
                return None
            
            closes = df['Close'].values[-252:]
            
            # OU process: dX = theta * (mu - X) * dt + sigma * dW
            # Linear regression of X(t) - X(t-1) on X(t-1)
            X = closes[:-1].reshape(-1, 1)
            Y = np.diff(closes)
            
            model = LinearRegression()
            model.fit(X, Y)
            
            # Y = a + b * X
            # b = -theta * dt -> theta = -b / dt
            # a = theta * mu * dt -> mu = a / (theta * dt) = -a / b
            dt = 1.0 / 252.0
            b = model.coef_[0]
            a = model.intercept_
            
            if b >= 0:
                # Not mean-reverting
                return None
                
            theta = -b / dt
            mu = -a / b
            
            residuals = Y - model.predict(X)
            sigma = np.std(residuals) / np.sqrt(dt)
            
            half_life = np.log(2) / theta
            
            current_price = closes[-1]
            deviation = (current_price / mu) - 1.0
            
            # Expected reversion
            expected_ret = -deviation * (1 - np.exp(-theta * (horizon / 252)))
            prob_up = 1.0 / (1.0 + np.exp(deviation * 10))
            
            pressure = "MODERATE"
            if abs(deviation) > 0.05: pressure = "HIGH"
            if abs(deviation) < 0.02: pressure = "LOW"
            
            return {
                "expected_return": expected_ret,
                "probability_up": prob_up,
                "name": "Mean Reversion",
                "details": {
                    "long_term_mean": float(mu),
                    "current_price": float(current_price),
                    "deviation": float(deviation),
                    "theta": float(theta),
                    "half_life": float(half_life * 252), # in days
                    "pressure": pressure
                }
            }
        except Exception as e:
            logger.error(f"Mean Reversion failed: {e}")
            return None

    def run_fama_french(self, df: pd.DataFrame) -> dict:
        try:
            import pandas_datareader.data as web
            import datetime
            
            if len(df) < 252:
                return None
                
            start = df.index[-252]
            ff = web.DataReader('F-F_Research_Data_5_Factors_2x3_daily', 'famafrench', start=start)
            ff_df = ff[0] / 100.0 # Convert from percentage to decimals
            
            asset_ret = df['Close'].pct_change().dropna()
            
            # Align dates
            aligned = pd.concat([asset_ret, ff_df], axis=1).dropna()
            if len(aligned) < 50:
                return None
                
            y = aligned['Close'] - aligned['RF']
            X = aligned[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']]
            X = sm.add_constant(X)
            
            model = sm.OLS(y, X).fit()
            
            return {
                "alpha": float(model.params['const'] * 252), # Annualized Alpha
                "market": float(model.params['Mkt-RF']),
                "size": float(model.params['SMB']),
                "value": float(model.params['HML']),
                "profitability": float(model.params['RMW']),
                "investment": float(model.params['CMA']),
                "name": "Fama-French"
            }
        except Exception as e:
            logger.error(f"Fama-French failed: {e}")
            return None

    def run_ols(self, df: pd.DataFrame, horizon: int) -> dict:
        try:
            if len(df) < horizon * 3:
                return None
            X = np.arange(len(df)).reshape(-1, 1)
            y = df['Close'].values
            model = LinearRegression()
            model.fit(X, y)
            current_price = y[-1]
            future_x = np.array([[len(df) + horizon - 1]])
            pred_price = model.predict(future_x)[0]
            expected_ret = (pred_price / current_price) - 1.0
            prob_up = 0.5 + (0.5 * np.sign(expected_ret) * min(abs(expected_ret)*5, 0.99))
            return {"expected_return": expected_ret, "probability_up": prob_up, "name": "Linear Regression"}
        except Exception as e:
            logger.error(f"OLS failed: {e}")
            return None

    def run_arima(self, df: pd.DataFrame, horizon: int) -> dict:
        try:
            if len(df) < 50:
                return None
            series = df['Close'].iloc[-252:]
            model = ARIMA(series, order=(1, 1, 1))
            res = model.fit()
            forecast = res.forecast(steps=horizon).iloc[-1]
            current_price = series.iloc[-1]
            expected_ret = (forecast / current_price) - 1.0
            prob_up = 0.5 + (np.sign(expected_ret) * 0.1)
            return {"expected_return": expected_ret, "probability_up": prob_up, "name": "ARIMA"}
        except Exception as e:
            logger.error(f"ARIMA failed: {e}")
            return None

    def run_lightgbm(self, df: pd.DataFrame, horizon: int) -> dict:
        try:
            if len(df) < 200:
                return None
            temp_df = df.copy()
            temp_df['ret'] = temp_df['Close'].pct_change()
            temp_df['target'] = temp_df['Close'].shift(-horizon) / temp_df['Close'] - 1.0
            temp_df['sma_20'] = temp_df['Close'].rolling(20).mean()
            temp_df['vol_20'] = temp_df['ret'].rolling(20).std()
            temp_df['mom_20'] = temp_df['Close'] / temp_df['Close'].shift(20) - 1.0
            train_df = temp_df.dropna()
            if len(train_df) < 50:
                return None
            features = ['ret', 'sma_20', 'vol_20', 'mom_20']
            X_train = train_df[features].values
            y_train = train_df['target'].values
            model = lgb.LGBMRegressor(n_estimators=50, max_depth=3, learning_rate=0.1, verbose=-1)
            model.fit(X_train, y_train)
            latest = temp_df.iloc[-1:][features].values
            pred_ret = model.predict(latest)[0]
            prob_up = 1.0 / (1.0 + np.exp(-pred_ret * 10))
            return {"expected_return": pred_ret, "probability_up": prob_up, "name": "LightGBM"}
        except Exception as e:
            logger.error(f"LightGBM failed: {e}")
            return None

    def run_xgboost(self, df: pd.DataFrame, horizon: int) -> dict:
        try:
            import xgboost as xgb
            if len(df) < 200:
                return None
            temp_df = df.copy()
            temp_df['ret'] = temp_df['Close'].pct_change()
            temp_df['target'] = (temp_df['Close'].shift(-horizon) / temp_df['Close'] - 1.0) / horizon
            temp_df['sma_20'] = temp_df['Close'].rolling(20).mean()
            temp_df['vol_20'] = temp_df['ret'].rolling(20).std()
            temp_df['mom_20'] = temp_df['Close'] / temp_df['Close'].shift(20) - 1.0
            train_df = temp_df.dropna()
            if len(train_df) < 50:
                return None
            features = ['ret', 'sma_20', 'vol_20', 'mom_20']
            X_train = train_df[features].values
            y_train = train_df['target'].values
            model = xgb.XGBRegressor(n_estimators=50, max_depth=3, learning_rate=0.1)
            model.fit(X_train, y_train)
            latest = temp_df.iloc[-1:][features].values
            pred_ret = model.predict(latest)[0] * horizon
            prob_up = 1.0 / (1.0 + np.exp(-pred_ret * 10))
            return {"expected_return": pred_ret, "probability_up": prob_up, "name": "XGBoost"}
        except Exception as e:
            logger.error(f"XGBoost failed: {e}")
            return None

    def run_random_forest(self, df: pd.DataFrame, horizon: int) -> dict:
        try:
            from sklearn.ensemble import RandomForestRegressor
            if len(df) < 200:
                return None
            temp_df = df.copy()
            temp_df['ret'] = temp_df['Close'].pct_change()
            temp_df['target'] = (temp_df['Close'].shift(-horizon) / temp_df['Close'] - 1.0) / horizon
            temp_df['sma_20'] = temp_df['Close'].rolling(20).mean()
            temp_df['vol_20'] = temp_df['ret'].rolling(20).std()
            temp_df['mom_20'] = temp_df['Close'] / temp_df['Close'].shift(20) - 1.0
            train_df = temp_df.dropna()
            if len(train_df) < 50:
                return None
            features = ['ret', 'sma_20', 'vol_20', 'mom_20']
            X_train = train_df[features].values
            y_train = train_df['target'].values
            model = RandomForestRegressor(n_estimators=50, max_depth=3)
            model.fit(X_train, y_train)
            latest = temp_df.iloc[-1:][features].values
            pred_ret = model.predict(latest)[0] * horizon
            prob_up = 1.0 / (1.0 + np.exp(-pred_ret * 10))
            return {"expected_return": pred_ret, "probability_up": prob_up, "name": "Random Forest"}
        except Exception as e:
            logger.error(f"RF failed: {e}")
            return None

    def run_garch(self, df: pd.DataFrame) -> dict:
        try:
            from arch import arch_model
            if len(df) < 252:
                return None
            ret = df['Close'].pct_change().dropna() * 100
            model = arch_model(ret, vol='Garch', p=1, q=1)
            res = model.fit(disp='off')
            
            # Forecast out 21 days
            forecasts = res.forecast(horizon=21)
            var_forecasts = forecasts.variance.values[-1, :]
            
            vol_1d = np.sqrt(var_forecasts[0]) / 100.0
            vol_5d = np.sqrt(var_forecasts[:5].sum()) / 100.0
            vol_21d = np.sqrt(var_forecasts.sum()) / 100.0
            
            regime = "HIGH" if vol_21d > 0.08 else "NORMAL"
            
            return {
                "expected_return": 0.0,
                "probability_up": 0.5,
                "name": "GARCH",
                "volatility": vol_21d,
                "details": {
                    "1D": float(vol_1d),
                    "5D": float(vol_5d),
                    "21D": float(vol_21d),
                    "regime": regime
                }
            }
        except Exception as e:
            logger.error(f"GARCH failed: {e}")
            return None
            
    def run_hmm(self, df: pd.DataFrame) -> dict:
        try:
            from hmmlearn.hmm import GaussianHMM
            if len(df) < 252:
                return None
            
            ret = df['Close'].pct_change().fillna(0).values.reshape(-1, 1)
            vol = df['Close'].pct_change().rolling(21).std().fillna(0).values.reshape(-1, 1)
            
            X = np.column_stack([ret, vol])
            
            # Using diag to prevent symmetric positive-definite errors on near-zero variance
            model = GaussianHMM(n_components=4, covariance_type="diag", n_iter=100, random_state=42)
            model.fit(X)
            
            hidden_states = model.predict(X)
            current_state = hidden_states[-1]
            
            # We must map states to semantic labels based on means and variances
            means = model.means_
            vars = model.covars_ # For diag, covars is (n_components, n_features)
            
            # Simple heuristic mapping
            state_metrics = []
            for i in range(4):
                state_metrics.append({
                    "state": i,
                    "mean_ret": means[i][0],
                    "mean_vol": vars[i][1] # Var of volatility
                })
                
            state_metrics.sort(key=lambda x: x["mean_ret"])
            
            # Lowest return is Bear, Highest is Bull.
            bear_state = state_metrics[0]["state"]
            bull_state = state_metrics[-1]["state"]
            
            # Of the remaining two, higher vol is High Vol
            rem = [s for s in state_metrics if s["state"] not in [bear_state, bull_state]]
            rem.sort(key=lambda x: x["mean_vol"])
            low_vol_state = rem[0]["state"]
            high_vol_state = rem[1]["state"]
            
            # Transition probabilities from current state
            trans = model.transmat_[current_state]
            
            probs = {
                "BULL": float(trans[bull_state]),
                "BEAR": float(trans[bear_state]),
                "HIGH VOL": float(trans[high_vol_state]),
                "LOW VOL": float(trans[low_vol_state])
            }
            
            labels_inv = {bull_state: "BULL", bear_state: "BEAR", high_vol_state: "HIGH VOL", low_vol_state: "LOW VOL"}
            current_regime = labels_inv[current_state]
            
            signal = "HOLD"
            if current_regime == "BULL": signal = "BUY"
            if current_regime == "BEAR": signal = "SELL"
            
            return {
                "regime": current_regime,
                "signal": signal,
                "strength": float(max(probs.values())),
                "name": "Regime",
                "probs": probs
            }
        except Exception as e:
            logger.error(f"HMM failed: {e}")
            return None

    def run_monte_carlo(self, mu: float, vol: float, current_price: float, horizon: int) -> dict:
        try:
            # GBM: S_T = S_0 * exp((mu - sigma^2/2) * T + sigma * W_T)
            n_paths = 10000
            T = horizon / 252.0
            
            # If horizon is too short or vol too small
            if T <= 0 or vol <= 0:
                return None
                
            drift = (mu - 0.5 * vol**2) * T
            shock = vol * np.sqrt(T) * np.random.normal(size=n_paths)
            
            prices = current_price * np.exp(drift + shock)
            returns = (prices / current_price) - 1.0
            
            prob_gt_10 = float(np.mean(returns > 0.10))
            prob_positive = float(np.mean(returns > 0.0))
            prob_lt_m10 = float(np.mean(returns < -0.10))
            median_ret = float(np.median(returns))
            
            return {
                "paths": n_paths,
                "prob_gt_10": prob_gt_10,
                "prob_positive": prob_positive,
                "prob_lt_m10": prob_lt_m10,
                "median_ret": median_ret
            }
        except Exception as e:
            logger.error(f"Monte Carlo failed: {e}")
            return None

    def execute_ensemble(self, df: pd.DataFrame, models: List[str], horizons: List[int]) -> dict:
        results = {}
        h = horizons[0] if len(horizons) > 0 else 21
        
        preds = []
        details = {}
        
        # Core Models
        res_mom = self.run_momentum(df, h)
        if res_mom: 
            preds.append(res_mom)
            details["momentum"] = res_mom.get("details")
            
        res_mr = self.run_mean_reversion(df, h)
        if res_mr: 
            preds.append(res_mr)
            details["mean_reversion"] = res_mr.get("details")
            
        res_ols = self.run_ols(df, h)
        if res_ols: preds.append(res_ols)
            
        res_arima = self.run_arima(df, h)
        if res_arima: preds.append(res_arima)
            
        res_lgb = self.run_lightgbm(df, h)
        if res_lgb: preds.append(res_lgb)
            
        res_xgb = self.run_xgboost(df, h)
        if res_xgb: preds.append(res_xgb)
            
        res_rf = self.run_random_forest(df, h)
        if res_rf: preds.append(res_rf)
            
        res_garch = self.run_garch(df)
        if res_garch:
            details["garch"] = res_garch.get("details")
            
        res_hmm = self.run_hmm(df)
        if res_hmm:
            details["hmm"] = res_hmm.get("probs")
            details["hmm_regime"] = res_hmm.get("regime")
            
        res_ff = self.run_fama_french(df)
        if res_ff:
            details["fama_french"] = res_ff
        
        if len(preds) > 0:
            # Ensemble weights (simple average for now, could be inverse variance)
            avg_ret = float(np.mean([p["expected_return"] for p in preds]))
            
            # Final signal via sigmoid
            # Normalize avg_ret to a Z-score roughly assuming std dev of 5%
            s_final = avg_ret / 0.05
            prob_bullish = 1.0 / (1.0 + np.exp(-s_final * 2))
            
            global_signal = "HOLD"
            if prob_bullish > 0.55: global_signal = "BULLISH"
            elif prob_bullish < 0.45: global_signal = "BEARISH"
                
            breakdown = []
            for p in preds:
                sig = "BUY" if p["probability_up"] > 0.55 else "SELL" if p["probability_up"] < 0.45 else "HOLD"
                strength = float(abs(p["probability_up"] - 0.5) * 2)
                breakdown.append({"name": p["name"], "signal": sig, "strength": max(0.1, min(1.0, strength))})
                
            if res_garch:
                vol21 = res_garch.get("volatility", 0.05)
                sig = "HIGH RISK" if vol21 > 0.08 else "LOW RISK"
                breakdown.append({"name": "GARCH", "signal": sig, "strength": min(1.0, vol21 * 10)})
                
            if res_hmm:
                breakdown.append({"name": "HMM Regime", "signal": res_hmm["signal"], "strength": res_hmm["strength"]})
                
            # Monte Carlo
            vol_estimate = res_garch.get("details", {}).get("21D", 0.05) if res_garch else 0.05
            mc_res = self.run_monte_carlo(avg_ret * (252/h), vol_estimate * np.sqrt(252/h), df['Close'].iloc[-1], h)
            if mc_res:
                details["monte_carlo"] = mc_res
                
            results["consensus"] = {
                "bullish_percent": float(np.mean([1 if p["probability_up"] > 0.5 else 0 for p in preds])),
                "breakdown": breakdown
            }
            results["expected_return"] = avg_ret
            results["probability_up"] = prob_bullish
            results["global_signal"] = global_signal
            results["current_regime"] = res_hmm["regime"] if res_hmm else "UNKNOWN"
            results["model_confidence"] = int(abs(prob_bullish - 0.5) * 200)
            results["details"] = details
            
        return results
