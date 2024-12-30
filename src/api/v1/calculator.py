import redis
import json
from src.models import Claim, ProviderAverage
from db import SessionDep
from sqlmodel import select
from publisher import publish


class Calculator:
    def __init__(self, session: SessionDep):
        self._session = session        
        

    def calculate_net_fee(self, claim: Claim):

        for item in claim.claims_process:            
            provider_average = self._get_provider_average(provider_npi=item.provider_npi)            
            net_fee = (item.provider_fees + item.member_coinsurance + item.member_copay) - item.allowed_fees
            
            provider_average.items += 1
            provider_average.total += net_fee
            provider_average.average = provider_average.total / provider_average.items            

            self._session.add(provider_average)
            self._session.commit()
            self._session.refresh(provider_average)

            publish(provider_average.model_dump_json())

    def _get_provider_average(self, provider_npi: int):
        
        statement = select(ProviderAverage).where(ProviderAverage.provider_npi==provider_npi)
        results = self._session.exec(statement).first()
        
        if results:
            return results
        return self._create_provider_average(provider_npi=provider_npi)

    def _create_provider_average(self, provider_npi: int):
        provider_average = ProviderAverage(provider_npi=provider_npi, average=0)

        self._session.add(provider_average)
        self._session.commit()

        return provider_average
    
