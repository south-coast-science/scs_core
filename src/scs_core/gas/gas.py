"""
Created on 13 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Conversion Factors Between ppb and μg m-3 and ppm and mgm-3 (EC, not WHO)

http://www.apis.ac.uk/unit-conversion
https://keisan.casio.com/exec/system/1224579725
"""


# --------------------------------------------------------------------------------------------------------------------

class Gas(object):
    """
    classdocs
    """

    STP_TEMPERATURE =       20.0                                # °C
    STP_PRESSURE =         101.3                                # kPa
    STP_MOLAR_VOLUME =      22.41                               # l

    ST_LAPSE_RATE =          0.0065                             # K/m
    GRAVITY =                9.80665                            # m/s2
    MOLAR_MASS_OF_AIR =     28.9644                             # g/mol
    GAS_CONSTANT =           8.3144598                          # J/(mol*K)


    # ----------------------------------------------------------------------------------------------------------------

    __NAMES = {'CO', 'CO2', 'NO', 'NO2', 'O3', 'Ox', 'SO2'}

    @classmethod
    def is_valid_name(cls, name):
        return name in cls.__NAMES


    # ----------------------------------------------------------------------------------------------------------------

    __MOLAR_DENSITY_STP = {
                'CO':   1.1642,
                'CO2':  1.9600,
                'NO':   1.3402,
                'NO2':  1.9125,
                'O3':   1.9957,
                'Ox':   1.9957,
                'SO2':  2.6609
    }

    @classmethod
    def __molar_density_stp(cls, gas):
        if gas not in cls.__MOLAR_DENSITY_STP:
            raise ValueError("Gas: unrecognised name: %s" % gas)

        return cls.__MOLAR_DENSITY_STP[gas]


    __MOLAR_MASS = {
                'CO':   28.0100,
                'CO2':  44.0100,
                'NO':   30.0100,
                'NO2':  46.0055,
                'O3':   48.0000,
                'Ox':   48.0000,
                'SO2':  64.0660
    }

    @classmethod
    def __molar_mass(cls, gas):
        if gas not in cls.__MOLAR_MASS:
            raise ValueError("Gas: unrecognised name: %s" % gas)

        return cls.__MOLAR_MASS[gas]


    @classmethod
    def __molar_volume(cls, t, p):
        tk = t + 273.15

        return cls.STP_MOLAR_VOLUME * (tk / 273.15) * (cls.STP_PRESSURE / p)


    # ----------------------------------------------------------------------------------------------------------------
    # density and concentration...

    @classmethod
    def concentration(cls, gas, density, t, p):                 # g/m3, °C, kPa -> ppb
        molar_mass = cls.__molar_mass(gas)
        molar_volume = cls.__molar_volume(t, p)

        molar_density = molar_mass / molar_volume

        return density / molar_density


    @classmethod
    def concentration_stp(cls, gas, density):                   # g/m3 -> ppb
        molar_density = cls.__molar_density_stp(gas)

        return density / molar_density


    @classmethod
    def density(cls, gas, concentration, t, p):                 # ppb, °C, kPa -> g/m3
        molar_mass = cls.__molar_mass(gas)
        molar_volume = cls.__molar_volume(t, p)

        molar_density = molar_mass / molar_volume

        return concentration * molar_density


    @classmethod
    def density_stp(cls, gas, concentration):                   # ppb -> g/m3
        molar_density = cls.__molar_density_stp(gas)

        return concentration * molar_density


    # ----------------------------------------------------------------------------------------------------------------
    # pressure...

    @classmethod
    def p_alt(cls, p_0, t, alt):                                # KPa, °C, m -> KPa
        return p_0 * cls.__hypsometric(t, alt)


    @classmethod
    def p_0(cls, p_alt, t, alt):                                # KPa, °C, m -> KPa
        return p_alt / cls.__hypsometric(t, alt)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __hypsometric(cls, t, alt):
        tk = t + 273.15
        lapse = alt * cls.ST_LAPSE_RATE
        a = (cls.GRAVITY * (cls.MOLAR_MASS_OF_AIR / 1000)) / (cls.GAS_CONSTANT * cls.ST_LAPSE_RATE)

        return pow(1 - (lapse / (tk + lapse)), a)
